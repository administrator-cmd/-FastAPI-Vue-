"""
用户相关 API 路由
遵循 RESTful 设计规范
使用统一响应格式
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.dependencies import get_async_db, get_current_user
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.repositories import user as user_crud
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.response import created, ok, unauthorized, server_error


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister, 
    db: AsyncSession = Depends(get_async_db)
):
    """
    用户注册
    POST /api/v1/users/register
    """
    logger.info(f"用户注册请求：用户名={user_data.username}, 邮箱={user_data.email}")
    
    try:
        db_user = await user_crud.create_user(
            db, 
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        logger.info(f"用户注册成功: ID={db_user.id}, 用户名={db_user.username}")
        
        response_data = UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at
        )
        
        return created(data=response_data.model_dump(), message="注册成功")
    except ValueError as e:
        logger.warning(f"用户注册失败: {str(e)} - 用户名={user_data.username}")
        return server_error(message=str(e))
    except Exception as e:
        logger.error(f"用户注册异常: {str(e)} - 用户名={user_data.username}")
        return server_error(message=f"创建用户失败: {str(e)}")


@router.post("/login")
async def login_user(
    login_data: UserLogin, 
    db: AsyncSession = Depends(get_async_db)
):
    """
    用户登录
    POST /api/v1/users/login
    """
    logger.info(f"用户登录请求：账户={login_data.account}")
    
    user = await user_crud.authenticate_user(db, login_data.account, login_data.password)
    if not user:
        logger.warning(f"登录失败: 账号或密码错误 - 账号={login_data.account}")
        return unauthorized(message="用户名或密码错误")

    logger.info(f"用户登录成功: ID={user.id}, 用户名={user.username}")

    from datetime import timedelta
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
    
    return ok(data=response_data, message="登录成功")


@router.get("/profile")
async def get_user_profile(current_user = Depends(get_current_user)):
    """
    获取当前用户信息
    GET /api/v1/users/profile
    """
    response_data = UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at
    )
    return ok(data=response_data.model_dump())


@router.get("")
async def list_users(db: AsyncSession = Depends(get_async_db)):
    """
    获取用户列表
    GET /api/v1/users
    """
    users = await user_crud.get_all_users(db)
    response_data = [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        ).model_dump()
        for user in users
    ]
    return ok(data=response_data)
