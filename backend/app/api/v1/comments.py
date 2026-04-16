"""
评论相关 API 路由
遵循 RESTful 设计规范
使用统一响应格式
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.dependencies import get_async_db, get_current_user_id
from app.schemas.comment import CommentCreate, CommentResponse
from app.repositories import comment as comment_crud
from app.repositories import post as post_crud
from app.schemas.response import created, ok, not_found, forbidden, server_error


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comments", tags=["评论管理"])


@router.post("/posts/{post_id}", status_code=201)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db)
):
    """
    创建评论
    POST /api/v1/comments/posts/{post_id}
    """
    post = await post_crud.get_post_by_id(db, post_id)
    if not post:
        return not_found(message="文章不存在")

    try:
        db_comment = await comment_crud.create_comment(
            db,
            content=comment_data.content,
            author_id=current_user_id,
            post_id=post_id
        )
        
        response_data = CommentResponse(
            id=db_comment.id,
            content=db_comment.content,
            author_id=db_comment.author_id,
            author_username=post.author.username if post.author else None,
            post_id=db_comment.post_id,
            created_at=db_comment.created_at
        )
        
        return created(data=response_data.model_dump(), message="评论创建成功")
    except ValueError as e:
        return server_error(message=str(e))
    except Exception as e:
        logger.error(f"创建评论失败: {str(e)}")
        return server_error(message=f"创建评论失败: {str(e)}")


@router.get("/posts/{post_id}")
async def get_comments(
    post_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取文章的评论列表
    GET /api/v1/comments/posts/{post_id}
    """
    comments = await comment_crud.get_comments(db, post_id)
    response_data = [
        CommentResponse(
            id=comment.id,
            content=comment.content,
            author_id=comment.author_id,
            author_username=comment.author.username if comment.author else None,
            post_id=comment.post_id,
            created_at=comment.created_at
        ).model_dump()
        for comment in comments
    ]
    return ok(data=response_data)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db)
):
    """
    删除评论
    DELETE /api/v1/comments/{comment_id}
    """
    comment = await comment_crud.get_comment_by_id(db, comment_id)
    if not comment:
        return not_found(message="评论不存在")

    if comment.author_id != current_user_id:
        return forbidden(message="无权限删除该评论")

    await comment_crud.delete_comment(db, comment_id, current_user_id)
    return ok(message="评论删除成功")
