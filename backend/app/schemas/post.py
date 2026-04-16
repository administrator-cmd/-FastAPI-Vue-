"""
文章相关的 Pydantic 模型
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.schemas.user import validate_content_safety


class PostCreate(BaseModel):
    """文章创建模型"""
    title: str = Field(..., min_length=5, max_length=200, description="文章标题")
    content: str = Field(..., min_length=10, description="文章内容")
    tag_names: Optional[List[str]] = Field(default=None, description="标签名称列表")

    @validator('title')
    def validate_title_safety(cls, v):
        """验证标题安全"""
        v = validate_content_safety(v)
        return v
    
    @validator('content')
    def validate_content_safety(cls, v):
        """验证内容安全"""
        v = validate_content_safety(v)
        if len(v) > 10000:
            raise ValueError('文章内容不能超过10000字')
        return v


class PostResponse(BaseModel):
    """文章响应模型"""
    id: int
    title: str
    content: str
    content_html: str
    author_id: int
    author_username: Optional[str] = None
    tags: List[dict] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
