"""
文章相关 API 路由
遵循 RESTful 设计规范
使用统一响应工具类
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.dependencies import get_async_db, get_current_user_id, verify_post_owner, get_pagination
from app.schemas.post import PostCreate, PostResponse
from app.repositories import post as post_crud
from app.repositories import tag as tag_crud
from app.schemas.response import success_response, error_response, created, not_found, server_error, ok

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["文章管理"])


@router.post("", status_code=201)
async def create_post(
    post_data: PostCreate, 
    current_user_id: int = Depends(get_current_user_id), 
    db: AsyncSession = Depends(get_async_db)
):
    """
    创建文章
    POST /api/v1/posts
    """
    try:
        # 1. 处理标签：先插入或获取标签对象
        tags = []
        if post_data.tag_names:
            for name in post_data.tag_names:
                tag_obj = await tag_crud.get_tag_by_name(db, name)
                if not tag_obj:
                    tag_obj = await tag_crud.create_tag(db, name)
                tags.append(tag_obj)
        
        # 2. 创建文章
        db_post = await post_crud.create_post(
            db,
            title=post_data.title,
            content=post_data.content,
            author_id=current_user_id,
            tags=tags
        )
        
        post_response = PostResponse(
            id=db_post.id,
            title=db_post.title,
            content=db_post.content,
            content_html=db_post.content_html,
            author_id=db_post.author_id,
            tags=[{"id": tag.id, "name": tag.name} for tag in db_post.tags],
            view_count=db_post.view_count,
            created_at=db_post.created_at,
            updated_at=db_post.updated_at
        )
        
        # 使用统一响应工具
        return created(data=post_response.model_dump(), message="文章创建成功")
        
    except ValueError as e:
        return error_response(message=str(e), code=400)
    except Exception as e:
        logger.error(f"创建文章失败: {str(e)}")
        return server_error(message=f"创建文章失败: {str(e)}")


@router.get("")
async def list_posts(
    pagination = Depends(get_pagination),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取文章列表（支持分页和搜索）
    GET /api/v1/posts?page=1&limit=10&keyword=xxx
    """
    posts = await post_crud.get_posts(
        db, 
        skip=pagination["skip"], 
        limit=pagination["limit"],
        keyword=keyword
    )
    
    post_list = [
        PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            content_html=post.content_html,
            author_id=post.author_id,
            author_username=post.author.username if post.author else None,
            tags=[{"id": tag.id, "name": tag.name} for tag in post.tags],
            view_count=post.view_count,
            created_at=post.created_at,
            updated_at=post.updated_at
        ).model_dump()
        for post in posts
    ]
    
    return success_response(data=post_list)


@router.get("/{post_id}")
async def get_post(post_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    获取单篇文章详情
    GET /api/v1/posts/{post_id}
    """
    post = await post_crud.get_post_by_id(db, post_id)
    if not post:
        return not_found(message="文章不存在")
    
    # 阅读量+1
    post.view_count += 1
    await db.commit()
    await db.refresh(post) # 刷新数据库
    
    post_response = PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        content_html=post.content_html,
        author_id=post.author_id,
        author_username=post.author.username if post.author else None,
        tags=[{"id": tag.id, "name": tag.name} for tag in post.tags],
        view_count=post.view_count,
        created_at=post.created_at,
        updated_at=post.updated_at
    )
    
    return success_response(data=post_response.model_dump())


@router.put("/{post_id}")
async def update_post(
    post_id: int, 
    post_data: PostCreate, 
    post = Depends(verify_post_owner),
    db: AsyncSession = Depends(get_async_db)
):
    """
    更新文章
    PUT /api/v1/posts/{post_id}
    """
    try:
        updated_post = await post_crud.update_post(
            db, 
            post_id, 
            title=post_data.title, 
            content=post_data.content
        )
        
        response_data = PostResponse(
            id=updated_post.id,
            title=updated_post.title,
            content=updated_post.content,
            content_html=updated_post.content_html,
            author_id=updated_post.author_id,
            tags=[{"id": tag.id, "name": tag.name} for tag in updated_post.tags],
            view_count=updated_post.view_count,
            created_at=updated_post.created_at,
            updated_at=updated_post.updated_at
        )
        
        return ok(data=response_data.model_dump(), message="文章更新成功")
    except Exception as e:
        logger.error(f"更新文章失败: {str(e)}")
        return server_error(message=f"更新文章失败: {str(e)}")


@router.delete("/{post_id}")
async def delete_post(    
    post_id: int, 
    post = Depends(verify_post_owner),
    db: AsyncSession = Depends(get_async_db)
):
    """
    删除文章
    DELETE /api/v1/posts/{post_id}
    """ 
    success = await post_crud.delete_post(db, post_id)
    if not success:
        return server_error(message="删除文章失败")
    
    return ok(message="文章删除成功")


@router.get("/user/{user_id}")
async def get_user_posts(user_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    获取指定用户的所有文章
    GET /api/v1/posts/user/{user_id}
    """
    from app.repositories import user as user_crud
    
    user = await user_crud.get_user_by_id(db, user_id)
    if not user:
        return not_found(message="用户不存在")
    
    posts = await post_crud.get_posts_by_user(db, user_id)
    response_data = [
        PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            content_html=post.content_html,
            author_id=post.author_id,
            author_username=post.author.username if post.author else None,
            tags=[{"id": tag.id, "name": tag.name} for tag in post.tags],
            view_count=post.view_count,
            created_at=post.created_at,
            updated_at=post.updated_at
        ).model_dump()
        for post in posts
    ]
    return ok(data=response_data)
