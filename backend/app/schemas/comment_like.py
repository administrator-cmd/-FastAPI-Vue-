from datetime import datetime

from pydantic import BaseModel

class CommentLikeRequest(BaseModel):
    """评论点赞请求模型"""
    comment_id: int

class CommentLikeResponse(BaseModel):
    """评论点赞模型"""
    id: int
    comment_id: int
    user_id: int
    created_at: datetime

class CommentLikeCount(BaseModel):
    """评论点赞数模型"""
    comment_id: int
    like_count: int