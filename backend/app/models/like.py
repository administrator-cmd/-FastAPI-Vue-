from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DATETIME, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship


class Like(Base):
    """点赞表"""
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True) # index=True 创建索引
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    author = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    # 唯一约束：同一个用户不能对同一篇文章重复点赞
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='uq_user_post_like'),
    )
    def __repr__(self):
        return f"<Like(id={self.id}, user_id={self.user_id}, post_id={self.post_id})>"