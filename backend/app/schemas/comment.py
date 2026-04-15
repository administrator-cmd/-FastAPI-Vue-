"""
评论相关的 Pydantic 模型
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.schemas.user import validate_content_safety


class CommentCreate(BaseModel):
    """评论创建模型"""
    content: str = Field(..., min_length=5, max_length=500, description="评论内容")
    
    @validator('content')
    def validate_content_safety(cls, v):
        """验证内容安全"""
        v = validate_content_safety(v)
        if len(v) > 1000:
            raise ValueError('评论内容不能超过1000字')
        return v


class CommentResponse(BaseModel):
    """评论响应模型"""
    id: int
    content: str
    author_id: int
    author_username: Optional[str] = None
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True
