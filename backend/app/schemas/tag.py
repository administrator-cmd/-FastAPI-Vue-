from datetime import datetime

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    """标签创建模型"""
    name: str = Field(..., min_length=1, max_length=50, description="标签名称")

class TagResponse(BaseModel):
    """标签响应模型"""
    id: int
    name: str
    created_at: datetime
    class Config:
        from_attributes = True