from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag


# 根据id获取标签
async def get_tag_by_id(db: AsyncSession, tag_id: int):
    result = await db.execute(select(Tag).filter(Tag.id == tag_id))
    return result.scalar_one_or_none()

# 根据名称获取标签
async def get_tag_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(Tag).filter(Tag.name == name))
    return result.scalar_one_or_none()

# 创建标签
async def create_tag(db: AsyncSession, name: str) -> Tag:
    tag_obj = Tag(name=name)
    db.add(tag_obj)
    await db.commit()
    await db.refresh(tag_obj)
    return tag_obj

# 获取所有标签
async def get_all_tags(db: AsyncSession) -> List[Tag]:
    result = await db.execute(select(Tag))
    return result.scalars().all()

# 根据id删除标签
async def delete_tag_by_id(db: AsyncSession, tag_id: int) -> bool:
    tag_obj = await get_tag_by_id(db, tag_id)
    await db.delete(tag_obj)
    await db.commit()
    return True