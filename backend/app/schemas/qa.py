from pydantic import Field
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    """
    提问请求模型
    """
    question: str = Field(...,min_length=1,description="用户问题")
    context: Optional[str] = Field(None,description="可选的上下文信息")

class AnswerResponse(BaseModel):
    """
    回答响应模型
    """
    id:int
    question: str
    answer: str = Field(...,min_length=1,description="AI回答")
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QAHistoryResponse(BaseModel):
    """
    问答历史记录模型
    """
    id: int
    question: str
    answer: str
    created_at: datetime

    class Config:
        from_attributes = True