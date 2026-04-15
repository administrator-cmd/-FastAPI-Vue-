"""
用户相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.dependencies import get_async_db, get_current_user
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.crud import user as user_crud
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister, 
    db: AsyncSession = Depends(get_async_db)
):
    """用户注册"""
    logger.info(f"用户注册请求：用户名={user_data.username}, 邮箱={user_data.email}")
    
    try:
        db_user = await user_crud.create_user(
            db, 
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        logger.info(f"用户注册成功: ID={db_user.id}, 用户名={db_user.username}")
        
        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at
        )
    except ValueError as e:
        logger.warning(f"用户注册失败: {str(e)} - 用户名={user_data.username}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"用户注册异常: {str(e)} - 用户名={user_data.username}")
        raise HTTPException(status_code=500, detail=f"创建用户失败: {str(e)}")


@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLogin, 
    db: AsyncSession = Depends(get_async_db)
):
    """用户登录"""
    logger.info(f"用户登录请求：账户={login_data.account}")
    
    user = await user_crud.authenticate_user(db, login_data.account, login_data.password)
    if not user:
        logger.warning(f"登录失败: 账号或密码错误 - 账号={login_data.account}")
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    logger.info(f"用户登录成功: ID={user.id}, 用户名={user.username}")

    from datetime import timedelta
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at
    )


@router.get("", response_model=List[UserResponse])
async def list_users(db: AsyncSession = Depends(get_async_db)):
    """获取用户列表"""
    users = await user_crud.get_all_users(db)
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
        for user in users
    ]
