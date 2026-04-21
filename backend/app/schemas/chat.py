from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatMesssageCreate(BaseModel):
    """创建聊天模型"""
    receiver_id: Optional[int] = None # NULL为群聊
    content: str = Field(..., description="内容")


class ChatMesssageResponse(BaseModel):
    """聊天消息响应"""
    id: int
    sender_id: int
    receiver_id: Optional[int]
    content: str
    created_at: datetime
    sender_name: str

    class Config:
        from_attributes = True
