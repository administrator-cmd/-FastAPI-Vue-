from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship

from app.core import Base


class ChatMessage(Base):
    """
    聊天消息表
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True) # 参数 index 表示创建索引
    sender_id = Column(Integer, ForeignKey("users.id"),nullable=False) #
    receiver_id = Column(Integer, ForeignKey("users.id"),nullable=True) # NULL 表示群聊
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),comment="创建时间")

    # 关系
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])