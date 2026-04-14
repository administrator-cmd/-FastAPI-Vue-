
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 定义与Post和Comment模型的一对多关系
    # 建立用户到文章的一对多关系，删除用户时，自动级联删除其所有文章，并通过 author 反向关联回用户
    posts = relationship("Post", back_populates="author",cascade="all,delete")
    #
    comments = relationship("Comment", back_populates="author")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False) # 原始Markdown文本
    content_html = Column(Text, nullable=False) # 渲染后的HTML文本
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="posts")
    # 定义文章到评论的一对多关系，删除文章时级联删除所有评论，且解除关联的孤立评论也会被自动删除，并通过 post 反向关联到文章。
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}, author_id={self.author_id})>"


class Comment(Base):
    """评论表"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)  # 评论内容
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 评论者ID
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)  # 文章ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    # 评论属于某个用户，通过 author 关联到 User 模型，User 那边用 comments 关联回来
    author = relationship("User", back_populates="comments")
    # 评论属于某个文章，通过 post 关联到 Post 模型，Post 那边用 comments 关联回来
    post = relationship("Post", back_populates="comments")
