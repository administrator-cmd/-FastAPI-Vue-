from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class QARecord(Base):
    """
    问答记录表
    存储用户问题和AI回答的历史记录
    """
    __tablename__ = "qa_records"

    id = Column(Integer, primary_key=True, index=True, comment="记录ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False, comment="用户ID")
    question = Column(Text, nullable= False,comment="用户问题")
    answer = Column(Text, nullable= False,comment="AI回答")
    context = Column(Text, nullable=True, comment="上下文信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(),comment="创建时间")

    # 关系： 关联到用户表
    user = relationship("User", back_populates="qa_records")

    def __repr__(self):
        return f"<QARecord(id={self.id}, user_id={self.user_id}, question={self.question}, answer={self.answer}, created_at={self.created_at})>"
