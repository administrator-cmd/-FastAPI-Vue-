"""
用户相关的 Pydantic 模型
"""
import re
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, validator


def validate_content_safety(content: str) -> str:
    """验证内容安全性，检查敏感词"""
    banned_words = ['黑胡子', '白胡子', '茶胡子']
    
    content_lower = content.lower()
    for banned_word in banned_words:
        if banned_word in content_lower:
            raise ValueError(f'内容中包含敏感词: {banned_word}')
    return content


class UserRegister(BaseModel):
    """用户注册模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=8, description="密码")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    bio: Optional[str] = Field(None, max_length=200, description="个人简介")

    @validator('password')
    def validate_password_strength(cls, v):
        """验证密码强度"""
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含至少一个数字')
        return v

    @validator('email')
    def validate_email_domain(cls, v):
        """验证邮箱域名限制"""
        domain = v.split('@')[1].lower()
        allowed_domains = [
            'gmail.com', 'qq.com', '163.com', '126.com',
            'outlook.com', 'hotmail.com', 'sina.com'
        ]
        
        if domain not in allowed_domains:
            allowed_list = ', '.join(allowed_domains)
            raise ValueError(f'不支持的邮箱域名，请使用以下邮箱: {allowed_list}')
        
        return v


class UserLogin(BaseModel):
    """用户登录模型"""
    account: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token 响应模型"""
    access_token: str
    token_type: str
    expires_in: int
