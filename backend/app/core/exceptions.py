"""
异常处理器模块
配合统一响应工具类使用，全局捕获异常并返回统一格式
"""
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.response import error_response, server_error

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    HTTP异常处理器
    
    处理 FastAPI 抛出的 HTTPException
    使用统一响应格式返回错误信息
    
    Args:
        request: FastAPI 请求对象
        exc: HTTP 异常对象
    
    Returns:
        JSONResponse: 统一格式的错误响应
    
    Example:
        抛出: HTTPException(status_code=404, detail="文章不存在")
        返回: {"code": 404, "message": "文章不存在", "data": null, "timestamp": xxx}
    """
    logger.error(
        "HTTP异常: %d - %s - 请求: %s %s",
        exc.status_code,
        exc.detail,
        request.method,
        request.url
    )
    
    # 使用统一响应工具返回
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=exc.detail, code=exc.status_code)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    数据验证异常处理器
    
    处理 Pydantic 模型验证失败的情况
    返回包含详细错误信息的统一响应
    
    Args:
        request: FastAPI 请求对象
        exc: 验证异常对象
    
    Returns:
        JSONResponse: 统一格式的验证错误响应
    """
    error_messages = [error['msg'] for error in exc.errors()]
    logger.warning(
        "数据验证失败: %s - 请求: %s %s",
        error_messages,
        request.method,
        request.url
    )

    # 使用统一响应工具，保留详细错误信息
    return JSONResponse(
        status_code=422,
        content=error_response(
            message="数据验证失败",
            code=422
        ) | {"details": error_messages}  # 合并额外字段
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    全局异常处理器
    
    捕获所有未处理的异常，返回友好错误信息
    避免暴露敏感的系统内部信息
    
    Args:
        request: FastAPI 请求对象
        exc: 异常对象
    
    Returns:
        JSONResponse: 统一格式的通用错误响应
    """
    logger.error(
        "未处理异常：%s: %s - 请求：%s %s",
        type(exc).__name__,
        str(exc),
        request.method,
        request.url,
        exc_info=True
    )
    
    # 使用统一响应工具返回
    return JSONResponse(
        status_code=500,
        content=server_error(message="服务器内部错误")
    )
