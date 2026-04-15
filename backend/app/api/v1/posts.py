"""
文章相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.dependencies import get_async_db, get_current_user_id, verify_post_owner, get_pagination
from app.schemas.post import PostCreate, PostResponse
from app.crud import post as post_crud


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["文章管理"])


@router.post("", response_model=PostResponse, status_code=201)
async def create_post(
    post_data: PostCreate, 
    current_user_id: int = Depends(get_current_user_id), 
    db: AsyncSession = Depends(get_async_db)
):
    """创建文章"""
    try:
        db_post = await post_crud.create_post(
            db,
            title=post_data.title,
            content=post_data.content,
            author_id=current_user_id
        )
        
        return PostResponse(
            id=db_post.id,
            title=db_post.title,
            content=db_post.content,
            content_html=db_post.content_html,
            author_id=db_post.author_id,
            created_at=db_post.created_at,
            updated_at=db_post.updated_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建文章失败: {str(e)}")


@router.get("", response_model=List[PostResponse])
async def list_posts(
    pagination = Depends(get_pagination),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: AsyncSession = Depends(get_async_db)
):
    """获取文章列表（支持分页和搜索）"""
    posts = await post_crud.get_posts(
        db, 
        skip=pagination["skip"], 
        limit=pagination["limit"],
        keyword=keyword
    )
    return [
        PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            content_html=post.content_html,
            author_id=post.author_id,
            author_username=post.author.username if post.author else None,
            created_at=post.created_at,
            updated_at=post.updated_at
        )
        for post in posts
    ]


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_async_db)):
    """获取单篇文章"""
    post = await post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        content_html=post.content_html,
        author_id=post.author_id,
        author_username=post.author.username if post.author else None,
        created_at=post.created_at,
        updated_at=post.updated_at
    )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int, 
    post_data: PostCreate, 
    post = Depends(verify_post_owner),
    db: AsyncSession = Depends(get_async_db)
):
    """更新文章"""
    try:
        updated_post = await post_crud.update_post(
            db, 
            post_id, 
            title=post_data.title, 
            content=post_data.content
        )
        
        return PostResponse(
            id=updated_post.id,
            title=updated_post.title,
            content=updated_post.content,
            content_html=updated_post.content_html,
            author_id=updated_post.author_id,
            created_at=updated_post.created_at,
            updated_at=updated_post.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新文章失败: {str(e)}")


@router.delete("/{post_id}")
async def delete_post(    
    post_id: int, 
    post = Depends(verify_post_owner),
    db: AsyncSession = Depends(get_async_db)
):
    """删除文章""" 
    success = await post_crud.delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除文章失败")
    
    return {"message": "文章删除成功"}


@router.get("/user/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(user_id: int, db: AsyncSession = Depends(get_async_db)):
    """获取指定用户的所有文章"""
    from app.crud import user as user_crud
    
    user = await user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    posts = await post_crud.get_posts_by_user(db, user_id)
    return [
        PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            content_html=post.content_html,
            author_id=post.author_id,
            created_at=post.created_at,
            updated_at=post.updated_at
        )
        for post in posts
    ]
