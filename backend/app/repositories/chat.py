from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chat import ChatMessage


# 创建聊天消息
async def create_chat_message(db: AsyncSession, sender_id: int, content: str, receiver_id: Optional[int] =  None) -> ChatMessage:
    db_message = ChatMessage(sender_id=sender_id, content=content, receiver_id=receiver_id)
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

# 获取聊天记录
async def get_chat_history(db: AsyncSession, sender_id: int, receiver_id: int = None) -> List[ChatMessage]:
    # 使用 selectinload 预加载 sender 关系，避免 async 模式下懒加载报错
    stmt = select(ChatMessage).options(selectinload(ChatMessage.sender))
    
    if receiver_id is not None:
        # 私聊：获取两人之间的所有消息
        stmt = stmt.filter(
            ((ChatMessage.sender_id == sender_id) & (ChatMessage.receiver_id == receiver_id)) |
            ((ChatMessage.sender_id == receiver_id) & (ChatMessage.receiver_id == sender_id))
        )
    else:
        # 不传 receiver_id 时，获取当前用户所有消息（包括群聊和私聊）
        stmt = stmt.filter(
            (ChatMessage.sender_id == sender_id) |
            (ChatMessage.receiver_id == sender_id)
        )
    stmt = stmt.order_by(ChatMessage.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()