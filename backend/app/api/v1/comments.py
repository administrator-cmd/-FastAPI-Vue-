"""
评论相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.dependencies import get_async_db, get_current_user_id
from app.schemas.comment import CommentCreate, CommentResponse
from app.crud import comment as comment_crud
from app.crud import post as post_crud


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comments", tags=["评论管理"])


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db)
):
    """创建评论"""
    post = await post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")

    try:
        db_comment = await comment_crud.create_comment(
            db,
            content=comment_data.content,
            author_id=current_user_id,
            post_id=post_id
        )
        return CommentResponse(
            id=db_comment.id,
            content=db_comment.content,
            author_id=db_comment.author_id,
            author_username=post.author.username if post.author else None,
            post_id=db_comment.post_id,
            created_at=db_comment.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建评论失败: {str(e)}")


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    post_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """获取文章的评论列表"""
    comments = await comment_crud.get_comments(db, post_id)
    return [
        CommentResponse(
            id=comment.id,
            content=comment.content,
            author_id=comment.author_id,
            author_username=comment.author.username if comment.author else None,
            post_id=comment.post_id,
            created_at=comment.created_at
        )
        for comment in comments
    ]


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db)
):
    """删除评论"""
    comment = await comment_crud.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    if comment.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="无权限删除该评论")

    await comment_crud.delete_comment(db, comment_id, current_user_id)
    return {"message": "评论删除成功"}
