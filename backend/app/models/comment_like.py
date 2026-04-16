from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class CommentLike(Base):
    """评论点赞表"""
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id",ondelete="CASCADE"), nullable=False) # 解释 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author = relationship("User",back_populates="comment_likes")

    __table_args__ = (
        UniqueConstraint('user_id', 'comment_id', name='uq_user_comment_like'),
    )
