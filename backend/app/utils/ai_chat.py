"""
AI 聊天工具类
封装云端 AI API 的调用逻辑
"""
import logging
from openai import OpenAI, AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

# 初始化异步客户端（复用连接）
client = AsyncOpenAI(
    api_key=settings.AI_API_KEY,
    base_url=settings.AI_BASE_URL
)


async def call_ai_api(question: str, context: str = None) -> str:
    """调用 AI API 获取回答"""
    messages = []
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": question})

    try:
        response = await client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"AI API 调用失败: {str(e)}")
        raise ValueError(f"AI 服务请求失败: {str(e)}")
