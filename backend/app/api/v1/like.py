"""
点赞相关API路由
"""
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import like
from app.dependencies import get_current_user_id, get_async_db
from app.schemas.like import LikeResponse, LikeCreate, LikePostCount

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/likes", tags=["点赞管理"])

# 创建点赞
@router.post("",response_model=LikeResponse, status_code=201)
async def create_like(
        like_data: LikeCreate,
        current_user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_db)
):
    """创建点赞"""
    logger.info(f"点赞用户id{current_user_id},点赞文章id{like_data.post_id}")
    # 查看文章是否存在
    post = await like.get_post_by_id(db, like_data.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    try:
        db_like = await like.create_like(db, current_user_id, like_data.post_id)
        logger.info(f"点赞成功,点赞ID={db_like.id},点赞用户ID={db_like.user_id},点赞文章ID={db_like.post_id}")
        return LikeResponse(
            id=db_like.id,
            post_id=db_like.post_id,
            user_id=db_like.user_id,
            created_at=db_like.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建点赞失败: {str(e)}")

# 取消点赞
@router.delete("/{like_id}")
async def delete_like(
        post_id: int,
        current_user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_db)
):
    """取消点赞"""
    logger.info(f"取消点赞用户id{current_user_id},点赞文章id{post_id}")
    # 查看点赞是否存在
    like_obj = await like.get_like_by_user_and_post(db, current_user_id, post_id)
    if not like_obj:
        raise HTTPException(status_code=404, detail="点赞不存在")
    try:
        success = await like.delete_like(db, current_user_id, post_id)
        if not success:
            raise HTTPException(status_code=500, detail="取消点赞失败")
        logger.info(f"取消点赞成功,点赞用户ID={current_user_id},点赞文章ID={post_id}")
        return {"message": "取消点赞成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消点赞失败: {str(e)}")

# 获取文章点赞数
@router.get("/{post_id}", response_model=LikePostCount)
async def get_post_like_count(
        post_id: int,
        db: AsyncSession = Depends(get_async_db)
):
    """获取文章点赞数"""
    logger.info(f"获取文章点赞数,文章ID={post_id}")
    # 查看文章是否存在
    post = await like.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    try:
        count = await like.get_post_like_count(db, post_id)
        return LikePostCount(
            post_id=post_id,
            like_count=count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文章点赞数失败: {str(e)}")


