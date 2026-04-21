import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect
from app.repositories import chat
from app.core.ConnectionManager import ConnectionManager
from app.dependencies import get_async_db, get_current_user_id
from app.utils.auth import get_current_user_from_ws
from app.schemas import ok, server_error

logger = logging.getLogger(__name__) # 创建日志记录器

router = APIRouter(prefix="/ws", tags=["websocket"])
manager = ConnectionManager()


@router.get("/chat/history")
async def get_chat_history_api(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db),
    receiver_id: int = Query(None, description="接收者ID，不传则获取群聊记录")
):
    """
    获取聊天记录 HTTP 接口
    """
    try:
        messages = await chat.get_chat_history(db, current_user_id, receiver_id)
        response_data = [
            {
                "id": msg.id,
                "sender_id": msg.sender_id,
                "receiver_id": msg.receiver_id,
                "content": msg.content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "sender_name": msg.sender.username if msg.sender else "未知用户"
            }
            for msg in messages
        ]
        return ok(data=response_data, message="获取聊天记录成功")
    except Exception as e:
        logger.error(f"获取聊天记录失败: {str(e)}")
        return server_error(message="获取聊天记录失败")


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket, db: AsyncSession = Depends(get_async_db)):
    """
    WebSocket 聊天端点
    连接示例: ws://localhost:8000/api/v1/ws/chat?token=your_jwt_token
    """
    logger.info(f"WebSocket 连接: {websocket.client.host}")
    # 从查询参数获取 token 并验证用户
    token = websocket.query_params.get("token")
    logger.info(f"Token 获取: {'有token' if token else '无token'}, 长度={len(token) if token else 0}")
    if not token:
        logger.warning("WebSocket 连接失败: 缺少 token")
        await websocket.close(code=1008)
        return

    try:
        user = await get_current_user_from_ws(token, db)
        logger.info(f"WebSocket 认证成功: user_id={user.id}, username={user.username}")
    except Exception as e:
        logger.error(f"WebSocket 认证失败: {str(e)}")
        await websocket.close(code=1008)
        return

    # 建立连接
    await manager.connect(websocket, user.id)

    try:
        while True:
            # 接收消息
            data = await websocket.receive_json()
            message_type = data.get("type")
            content = data.get("content")

            if message_type == "chat_message":
                # 保存消息到数据库
                receiver_id = data.get("receiver_id")
                db_message = await chat.create_chat_message(
                    db=db,
                    sender_id=user.id,
                    content=content,
                    receiver_id=receiver_id
                )

                # 构建消息对象
                message_data = {
                    "type": "new_message",
                    "id": db_message.id,
                    "sender_id": db_message.sender_id,
                    "receiver_id": db_message.receiver_id,
                    "content": db_message.content,
                    "created_at": db_message.created_at.isoformat(),
                    "sender_name": user.username
                }

                # 发送给接收者（私聊）或广播（群聊）
                if receiver_id:
                    await manager.send_personal_message(message_data, receiver_id)
                    # 也发送给发送者
                    await manager.send_personal_message(message_data, user.id)
                else:
                    # 群聊广播给所有人
                    await manager.broadcast(message_data)

            elif message_type == "ping":
                # 心跳检测
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)