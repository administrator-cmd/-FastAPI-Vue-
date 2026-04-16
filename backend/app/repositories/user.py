"""
用户相关的 CRUD 操作
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional
import hashlib

from app.models.user import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """异步根据ID获取用户"""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """异步根据用户名获取用户"""
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """异步根据邮箱获取用户"""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()


async def get_user_count(db: AsyncSession) -> int:
    """异步获取用户总数"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return len(users)


async def get_all_users(db: AsyncSession) -> List[User]:
    """异步获取所有用户"""
    result = await db.execute(select(User))
    return result.scalars().all()


async def create_user(db: AsyncSession, username: str, email: str, password: str) -> User:
    """异步创建用户"""
    # 检查用户名是否已存在
    existing_user = await get_user_by_username(db, username)
    if existing_user:
        raise ValueError("用户名已存在")
    
    # 检查邮箱是否已被注册
    existing_email = await get_user_by_email(db, email)
    if existing_email:
        raise ValueError("邮箱已被注册")
    
    # 密码哈希
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


async def authenticate_user(db: AsyncSession, account: str, password: str) -> Optional[User]:
    """异步用户认证 - 支持用户名或邮箱登录"""
    result = await db.execute(
        select(User).filter(
            or_(User.username == account, User.email == account)
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    # 验证密码
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user.hashed_password != password_hash:
        return None
    
    return user
