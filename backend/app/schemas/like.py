from datetime import datetime

from pydantic import BaseModel


class LikeCreate(BaseModel):
    """点赞创建模型"""
    post_id: int

class LikeResponse(BaseModel):
    """点赞响应模型"""
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        # orm_mode = True v1版本配置
        from_attributes = True
class LikePostCount(BaseModel):
    """点赞数响应模型"""
    post_id: int
    like_count: int
