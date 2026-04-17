"""
博客系统API - FastAPI应用入口
模块化架构版本
"""
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import time

from app.core.database import create_tables
from app.dependencies import get_async_db
from app.api.v1 import users, posts, comments, like, comment_like, tags, qa
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler
)
import fastapi_cdn_host


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="博客系统API",
    description="基于 FastAPI + SQLAlchemy 的模块化博客系统",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CDN 优化（加速 Swagger 文档加载）
fastapi_cdn_host.patch_docs(app)

logger.info("✓ CORS 中间件已配置")


# ===== 中间件 =====

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """请求日志中间件 - 记录所有请求的详细信息"""
    start_time = time.time()
    
    logger.info(
        "请求开始: %s %s - 客户端: %s",
        request.method, 
        request.url, 
        request.client.host if request.client else 'unknown'
    )

    response = await call_next(request)
    process_time = time.time() - start_time

    status_text = "成功" if response.status_code < 400 else "失败"

    logger.info(
        "请求完成(%s): %s %s - 状态码: %d - 耗时: %.4f秒",
        status_text,
        request.method, 
        request.url, 
        response.status_code, 
        process_time
    )
    
    response.headers["X-Process-Time"] = str(process_time)

    if process_time > 1:
        logger.warning(
            "慢请求警告: %s %s 耗时 %.4f秒，建议优化",
            request.method, 
            request.url, 
            process_time
        )

    return response


# ===== 异常处理 =====
# 注册异常处理器（从 utils.exceptions 导入）

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


# ===== 应用启动事件 =====

@app.on_event("startup")
async def startup_event():
    """应用启动时创建数据表"""
    await create_tables()
    logger.info("✓ 数据库表创建完成")


# ===== 根路由 =====

@app.get("/")
async def root():
    """欢迎页面"""
    logger.info("访问根路由")
    return {
        "message": "欢迎使用博客系统API",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "用户管理", 
            "文章管理", 
            "评论管理",
            "点赞功能",
            "JWT认证",
            "Markdown支持"
        ]
    }


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_async_db)):
    """健康检查API - 用于监控服务状态"""
    try:
        from app.repositories import user as user_crud
        from app.repositories import post as post_crud
        
        user_count = await user_crud.get_user_count(db)
        post_count = await post_crud.get_post_count(db)
        
        logger.info(f"健康检查通过：用户数={user_count}, 文章数={post_count}")
        
        return {
            "status": "healthy",
            "version": "1.0.0",
            "users_count": user_count,
            "posts_count": post_count,
            "database": "SQLite (Async)",
            "architecture": "Modular"
        }
    except Exception as e:
        logger.error(f"健康检查失败：{str(e)}")
        raise HTTPException(status_code=503, detail="服务不可用")


# ===== 注册路由 =====

# 注册 v1 API 路由
app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")
app.include_router(like.router, prefix="/api/v1")
app.include_router(comment_like.router, prefix="/api/v1")
app.include_router(tags.router, prefix="/api/v1")
app.include_router(qa.router, prefix="/api/v1")

logger.info("✓ API路由注册完成")
logger.info("✓ 博客系统启动成功")
