"""
文章相关的 CRUD 操作
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from typing import List, Optional

from sqlalchemy.orm import joinedload

from app.models.post import Post
from app.models.user import User
from app.models.tag import Tag, post_tags
from app.utils.markdown import render_markdown
from app.repositories import user as user_crud
from app.repositories import tag as tag_crud
from app.repositories import comment as comment_crud


async def get_post_by_id(db: AsyncSession, post_id: int) -> Optional[Post]:
    """异步根据ID获取文章"""
    result = await db.execute(
        select(Post).filter(Post.id == post_id).options(joinedload(Post.author), joinedload(Post.tags))
    )
    return result.unique().scalar_one_or_none()


async def get_posts_by_user(db: AsyncSession, user_id: int) -> List[Post]:
    """异步获取指定用户的所有文章"""
    result = await db.execute(
        select(Post).filter(Post.author_id == user_id).order_by(desc(Post.created_at)).options(joinedload(Post.tags))
    )
    return result.unique().scalars().all()


async def get_posts(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100, 
    keyword: str = None
) -> List[Post]:
    """异步获取文章列表（支持分页和搜索）"""
    query = select(Post).options(joinedload(Post.author), joinedload(Post.tags))

    if keyword and keyword.strip():
        query = query.filter(
            or_(
                Post.title.contains(keyword),
                Post.content.contains(keyword)
            )
        )
    
    query = query.order_by(desc(Post.created_at)).offset(skip).limit(limit)
        
    result = await db.execute(query)
    return result.unique().scalars().all()


async def get_post_count(db: AsyncSession) -> int:
    """异步获取文章总数"""
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return len(posts)


async def create_post(db: AsyncSession, title: str, content: str, author_id: int, tags: List["Tag"] = None) -> Post:
    """异步创建文章"""
    author = await user_crud.get_user_by_id(db, author_id)
    if not author:
        raise ValueError("作者不存在")
    
    db_post = Post(
        title=title,
        content=content,
        content_html=render_markdown(content),
        author_id=author_id,
        tags=tags or []  # 直接绑定标签对象列表
    )
    
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    
    return db_post


async def update_post(
    db: AsyncSession, 
    post_id: int, 
    title: str = None, 
    content: str = None
) -> Optional[Post]:
    """异步更新文章"""
    post = await get_post_by_id(db, post_id)
    if not post:
        return None
    
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content
    post.content_html = render_markdown(post.content)
    await db.commit()
    await db.refresh(post)
    
    return post


async def delete_post(db: AsyncSession, post_id: int) -> bool:
    """异步删除文章"""
    post = await get_post_by_id(db, post_id)
    if not post:
        return False
    
    await db.delete(post)
    await db.commit()
    
    return True
