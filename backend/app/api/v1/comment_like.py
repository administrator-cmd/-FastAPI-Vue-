"""
评论点赞相关 API 路由
遵循 RESTful 设计规范
使用统一响应格式
"""
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import comment_like
from app.dependencies import get_current_user_id, get_async_db
from app.schemas.comment_like import CommentLikeCount, CommentLikeResponse, CommentLikeRequest
from app.schemas.response import created, ok, not_found, server_error

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comment-likes", tags=["评论点赞管理"])

@router.post("", status_code=201)
async def create_comment_like(
        request_data: CommentLikeRequest,
        current_user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_db)
):
    """
    创建评论点赞
    POST /api/v1/comment-likes
    """
    logger.info(f"创建评论点赞,用户ID={current_user_id},评论ID={request_data.comment_id}")
    try:
        db_comment_like = await comment_like.create_comment_like(db, request_data.comment_id, current_user_id)
        logger.info(f"创建评论点赞成功,用户ID={current_user_id},评论ID={request_data.comment_id}")
        
        response_data = CommentLikeResponse(
            id=db_comment_like.id,
            comment_id=db_comment_like.comment_id,
            user_id=db_comment_like.user_id,
            created_at=db_comment_like.created_at
        )
        
        return created(data=response_data.model_dump(), message="评论点赞成功")
    except ValueError as e:
        return server_error(message=str(e))
    except Exception as e:
        logger.error(f"创建评论点赞失败: {str(e)}")
        return server_error(message=f"创建评论点赞失败: {str(e)}")

@router.delete("/{comment_id}")
async def delete_comment_like(
        comment_id: int,
        current_user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_db)
):
    """
    取消评论点赞
    DELETE /api/v1/comment-likes/{comment_id}
    """
    logger.info(f"取消评论点赞,用户ID={current_user_id},评论ID={comment_id}")
    try:
        success = await comment_like.delete_comment_like(db, comment_id, current_user_id)
        if not success:
            return not_found(message="点赞记录不存在")
        
        logger.info(f"取消评论点赞成功,用户ID={current_user_id},评论ID={comment_id}")
        return ok(message="取消评论点赞成功")
    except Exception as e:
        logger.error(f"取消评论点赞失败: {str(e)}")
        return server_error(message=f"取消评论点赞失败: {str(e)}")


@router.get("/{comment_id}")
async def get_comment_like_count(
        comment_id: int,
        db: AsyncSession = Depends(get_async_db)
):
    """
    获取评论点赞数
    GET /api/v1/comment-likes/{comment_id}
    """
    logger.info(f"获取评论点赞数,评论ID={comment_id}")
    try:
        count = await comment_like.get_comment_like_count(db, comment_id)
        response_data = CommentLikeCount(
            comment_id=comment_id,
            like_count=count
        )
        return ok(data=response_data.model_dump())
    except Exception as e:
        logger.error(f"获取评论点赞数失败: {str(e)}")
        return server_error(message=f"获取评论点赞数失败: {str(e)}")


@router.get("/user/{comment_id}")
async def get_user_comment_like_status(
        comment_id: int,
        current_user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_db)
):
    """
    获取当前用户对某条评论的点赞状态
    GET /api/v1/comment-likes/user/{comment_id}
    """
    logger.info(f"获取用户评论点赞状态,用户ID={current_user_id},评论ID={comment_id}")
    try:
        like_obj = await comment_like.get_comment_like_by_user_and_comment(db, comment_id, current_user_id)
        return ok(data={"comment_id": comment_id, "is_liked": like_obj is not None})
    except Exception as e:
        logger.error(f"获取评论点赞状态失败: {str(e)}")
        return server_error(message=f"获取评论点赞状态失败: {str(e)}")