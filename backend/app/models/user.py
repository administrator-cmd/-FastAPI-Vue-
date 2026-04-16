"""
用户数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 定义与Post和Comment模型的一对多关系
    posts = relationship("Post", back_populates="author", cascade="all,delete-orphan") # 解释： 删除用户时，删除用户下的所有文章
    comments = relationship("Comment", back_populates="author", cascade="all,delete-orphan") # 解释： 删除用户时，删除用户下的所有评论

    # 定义与Like模型的一对多关系
    likes = relationship("Like", back_populates="author", cascade="all,delete-orphan") # 解释： 删除用户时，删除用户下的所有点赞记录
    # 定义与CommentLike模型的一对多关系
    comment_likes = relationship("CommentLike", back_populates="author", cascade="all,delete-orphan")
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
