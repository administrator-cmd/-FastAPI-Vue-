"""
点赞相关 API 路由
遵循 RESTful 设计规范
使用统一响应格式
"""
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import like
from app.dependencies import get_current_user_id, get_async_db
from app.schemas.like import LikeResponse, LikeCreate, LikePostCount
from app.schemas.response import created, ok, not_found, server_error

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/likes", tags=["点赞管理"])

@router.post("", status_code=201)
async def create_like(
        like_data: LikeCreate,
        current_user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_db)
):
    """
    创建点赞
    POST /api/v1/likes
    """
    logger.info(f"点赞用户id{current_user_id},点赞文章id{like_data.post_id}")
    # 查看文章是否存在
    post = await like.get_post_by_id(db, like_data.post_id)
    if not post:
        return not_found(message="文章不存在")
    try:
        db_like = await like.create_like(db, current_user_id, like_data.post_id)
        logger.info(f"点赞成功,点赞ID={db_like.id},点赞用户ID={db_like.user_id},点赞文章ID={db_like.post_id}")
        
        response_data = LikeResponse(
            id=db_like.id,
            post_id=db_like.post_id,
            user_id=db_like.user_id,
            created_at=db_like.created_at
        )
        
        return created(data=response_data.model_dump(), message="点赞成功")
    except ValueError as e:
        return server_error(message=str(e))
    except Exception as e:
        logger.error(f"创建点赞失败: {str(e)}")
        return server_error(message=f"创建点赞失败: {str(e)}")

@router.delete("/{post_id}")
async def delete_like(
        post_id: int,
        current_user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_db)
):
    """
    取消点赞
    DELETE /api/v1/likes/{post_id}
    """
    logger.info(f"取消点赞用户id{current_user_id},点赞文章id{post_id}")
    # 查看点赞是否存在
    like_obj = await like.get_like_by_user_and_post(db, current_user_id, post_id)
    if not like_obj:
        return not_found(message="还没有点赞")
    try:
        success = await like.delete_like(db, current_user_id, post_id)
        if not success:
            return server_error(message="取消点赞失败")
        logger.info(f"取消点赞成功,点赞用户ID={current_user_id},点赞文章ID={post_id}")
        return ok(message="取消点赞成功")
    except Exception as e:
        logger.error(f"取消点赞失败: {str(e)}")
        return server_error(message=f"取消点赞失败: {str(e)}")

@router.get("/user/{post_id}")
async def get_user_like_status(
        post_id: int,
        current_user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_db)
):
    """
    获取当前用户对某篇文章的点赞状态
    GET /api/v1/likes/user/{post_id}
    """
    logger.info(f"获取用户点赞状态,用户ID={current_user_id},文章ID={post_id}")
    try:
        like_obj = await like.get_like_by_user_and_post(db, current_user_id, post_id)
        return ok(data={"post_id": post_id, "is_liked": like_obj is not None})
    except Exception as e:
        logger.error(f"获取点赞状态失败: {str(e)}")
        return server_error(message=f"获取点赞状态失败: {str(e)}")


@router.get("/{post_id}")
async def get_post_like_count(
        post_id: int,
        db: AsyncSession = Depends(get_async_db)
):
    """
    获取文章点赞数
    GET /api/v1/likes/{post_id}
    """
    logger.info(f"获取文章点赞数,文章ID={post_id}")
    # 查看文章是否存在
    post = await like.get_post_by_id(db, post_id)
    if not post:
        return not_found(message="文章不存在")
    try:
        count = await like.get_post_like_count(db, post_id)
        response_data = LikePostCount(
            post_id=post_id,
            like_count=count
        )
        return ok(data=response_data.model_dump())
    except Exception as e:
        logger.error(f"获取文章点赞数失败: {str(e)}")
        return server_error(message=f"获取文章点赞数失败: {str(e)}")


