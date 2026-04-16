import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_db
from app.repositories import tag
from app.schemas import error_response, ok, created
from app.schemas.tag import TagCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tags", tags=["标签管理"])

# 创建标签
@router.post("", status_code=201)
async def create_tag(tag_data: TagCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        if_existed = await tag.get_tag_by_name(db, tag_data.name)
        if if_existed:
            return error_response(message="标签已存在")
        tag_obj = await tag.create_tag(db, tag_data.name)
        logger.info(f"创建标签成功: {tag_obj.name}")
        return created(data=tag_obj.model_dump(), message="创建标签成功")
    except ValueError as e:
        logger.error(f"创建标签失败: {str(e)}")
    except Exception as e:
        logger.error(f"创建标签失败: {e}")
        return error_response(message="创建标签失败")

# 获取所有标签
@router.get("")
async def get_all_tags(db: AsyncSession = Depends(get_async_db)):
    try:
        tags = await tag.get_all_tags(db)
        logger.info(f"获取所有标签成功: {len(tags)}")
        return ok(data=[tag_obj.model_dump() for tag_obj in tags], message="获取所有标签成功")
    except Exception as e:
        logger.error(f"获取所有标签失败: {str(e)}")
        return error_response(message="获取所有标签失败")

# 获取单个标签
@router.get("/{tag_id}")
async def get_tag_by_id(tag_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        tag_obj = await tag.get_tag_by_id(db,tag_id)
        if not tag_obj:
            return error_response(message="标签不存在")
        logger.info(f"获取标签成功: {tag_obj.name}")
        return ok(data=tag_obj.model_dump(), message="获取标签成功")
    except Exception as e:
        logger.error(f"获取标签失败: {str(e)}")
        return error_response(message="获取标签失败")
