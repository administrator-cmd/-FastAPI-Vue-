"""
统一响应工具类
提供手动封装的响应辅助函数
"""
import time
from typing import Optional, Any, Generic, TypeVar
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    统一API响应模型
    
    Attributes:
        code: 业务状态码（200成功，其他为错误码）
        message: 响应消息
        data: 业务数据（可选）
        timestamp: 时间戳（毫秒）
    
    Example:
        {
            "code": 200,
            "message": "操作成功",
            "data": {"id": 1, "title": "文章"},
            "timestamp": 1713168000000
        }
    """
    code: int = Field(default=200, description="业务状态码")
    message: str = Field(default="操作成功", description="响应消息")
    data: Optional[Any] = Field(default=None, description="业务数据")
    timestamp: int = Field(
        default_factory=lambda: int(time.time() * 1000), # 毫秒级时间戳
        description="时间戳（毫秒）"
    )


def success_response(data: Any = None, message: str = "操作成功") -> dict:
    """
    成功响应辅助函数
    
    Args:
        data: 业务数据
        message: 成功消息
    
    Returns:
        dict: 统一格式的成功响应字典
    
    Example:
        return success_response(data={"id": 1}, message="创建成功")
    """
    return ApiResponse(
        code=200,
        message=message,
        data=data
    ).model_dump()


def error_response(message: str, code: int = 400) -> dict:
    """
    错误响应辅助函数
    
    Args:
        message: 错误消息
        code: 错误码（默认400）
    
    Returns:
        dict: 统一格式的错误响应字典
    
    Example:
        return error_response(message="参数错误", code=400)
    """
    return ApiResponse(
        code=code,
        message=message,
        data=None
    ).model_dump()


# 常用快捷函数
def ok(data: Any = None, message: str = "操作成功") -> dict:
    """成功响应快捷方式"""
    return success_response(data=data, message=message)


def created(data: Any = None, message: str = "创建成功") -> dict:
    """创建成功快捷方式（HTTP 201）"""
    response = success_response(data=data, message=message)
    response['code'] = 201
    return response


def bad_request(message: str = "请求参数错误") -> dict:
    """请求错误快捷方式（400）"""
    return error_response(message=message, code=400)


def unauthorized(message: str = "未授权，请先登录") -> dict:
    """未授权快捷方式（401）"""
    return error_response(message=message, code=401)


def forbidden(message: str = "权限不足") -> dict:
    """禁止访问快捷方式（403）"""
    return error_response(message=message, code=403)


def not_found(message: str = "资源不存在") -> dict:
    """资源不存在快捷方式（404）"""
    return error_response(message=message, code=404)


def server_error(message: str = "服务器内部错误") -> dict:
    """服务器错误快捷方式（500）"""
    return error_response(message=message, code=500)
