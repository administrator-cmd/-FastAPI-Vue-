"""
应用配置模块
集中管理所以环境变量和配置项
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


def get_env(key: str, required: bool = True) -> str:
    """获取环境变量"""
    value = os.getenv(key)
    if required and value is None:
        raise ValueError(f"环境变量 {key} 未设置")
    return value

class Settings:
    """应用配置类"""

    # ===== 数据库配置（必需）=====
    DATABASE_URL: str = get_env("DATABASE_URL")

    # ===== AI API 配置（必需）=====
    AI_API_KEY: str = get_env("AI_API_KEY")
    AI_BASE_URL: str = get_env("AI_BASE_URL")
    AI_MODEL: str = get_env("AI_MODEL")

    # ===== JWT 配置（必需）=====
    SECRET_KEY: str = get_env("SECRET_KEY")
    ALGORITHM: str = get_env("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_env("ACCESS_TOKEN_EXPIRE_MINUTES"))

# 创建应用配置对象
settings = Settings()
