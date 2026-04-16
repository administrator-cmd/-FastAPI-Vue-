"""
评论相关的 CRUD 操作
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional

from sqlalchemy.orm import joinedload

from app.models.comment import Comment


async def create_comment(
    db: AsyncSession, 
    content: str, 
    author_id: int, 
    post_id: int
) -> Comment:
    """异步创建评论"""
    db_comment = Comment(
        content=content,
        author_id=author_id,
        post_id=post_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def get_comments(db: AsyncSession, post_id: int) -> List[Comment]:
    """异步获取文章的评论列表"""
    result = await db.execute(
        select(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.post_id == post_id)
        .order_by(desc(Comment.created_at))
    )
    return result.unique().scalars().all()


async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Optional[Comment]:
    """根据id获取对应的评论"""
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    return result.scalar_one_or_none()


async def delete_comment(db: AsyncSession, comment_id: int, author_id: int) -> bool:
    """删除评论"""
    result = await db.execute(
        select(Comment).filter(
            Comment.id == comment_id, 
            Comment.author_id == author_id
        )
    )
    comment = result.scalar_one_or_none()
    if comment:
        await db.delete(comment)
        await db.commit()
        return True
    return False
