"""
    点赞相关的CRUD
"""
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_post_by_id, get_user_by_id
from app.models.like import Like

# type: ignore 用于忽略 SQLAlchemy 的类型检查警告

# 创建点赞
async def create_like(db: AsyncSession, user_id: int, post_id: int) -> Like:
    # 先验证文章是否存在
    post = await get_post_by_id(db, post_id)
    if not post:
        raise ValueError("文章不存在")
    # 再验证用户是否存在
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("用户不存在")
    db_like = Like(
        user_id = user_id,
        post_id = post_id
    )
    db.add(db_like)
    await db.commit()
    await db.refresh(db_like)
    return db_like
# 获取点赞
async def get_like_by_user_and_post(db: AsyncSession, user_id: int, post_id: int) -> Optional[Like]:
    """查询用户是否已点赞同篇文章"""
    result = await db.execute(
        select(Like).filter(
            Like.user_id == user_id,
            Like.post_id == post_id
        )
    )
    return result.scalar_one_or_none()

# 删除点赞
async def delete_like(db: AsyncSession,user_id: int, post_id: int) -> bool:
    """异步删除点赞 只能删除自己的点赞"""
    like =  Like.get_like_by_user_and_post(db, user_id, post_id)
    if not like:
        return False

    await db.delete(like)
    await db.commit()

    return  True
# 获取文章点赞数
async def get_post_like_count(db: AsyncSession, post_id: int) -> int:
    """获取文章点赞数"""
    result = await db.execute(
        select(func.count(Like.id)).filter(
            Like.post_id == post_id
        )
    )
    return result.scalar_one() or 0