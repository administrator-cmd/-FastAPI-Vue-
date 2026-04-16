from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.comment_like import CommentLike
from app.schemas.comment_like import CommentLikeResponse


# 新增评论点赞
async def create_comment_like(
    db: AsyncSession,
    comment_id: int,
    user_id: int
) -> CommentLike:
    """新增评论点赞"""
    comment_like_obj = CommentLike(
        comment_id=comment_id,
        user_id=user_id
    )
    db.add(comment_like_obj)
    await db.commit()
    await db.refresh(comment_like_obj)
    return comment_like_obj

# 取消评论点赞
async def get_comment_like_by_user_and_comment(db, current_user_id, comment_id) -> Optional[CommentLike]:
    commentlike_obj = await db.execute(
        select(CommentLike).filter(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == current_user_id
        )
    )
    return commentlike_obj.scalar_one_or_none()


async def delete_comment_like(db : AsyncSession, comment_id : int, current_user_id : int) -> bool:
    """取消评论点赞"""
    commentlike_obj = await get_comment_like_by_user_and_comment(db, current_user_id, comment_id)
    if not commentlike_obj:
        return False
    await db.delete(commentlike_obj)
    await db.commit()
    return True


async def get_comment_like_count(db: AsyncSession, comment_id: int) -> int:
    """获取评论点赞数"""
    result = await db.execute(
        select(func.count()).select_from(CommentLike).filter(
            CommentLike.comment_id == comment_id
        )
    )
    return result.scalar_one()


# 别名函数，保持命名一致性
get_comment_like_by_user_and_comment = get_comment_like_by_user_and_comment
