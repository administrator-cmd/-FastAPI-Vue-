import logging

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_async_db, get_current_user_id
from app.repositories import qa
from app.schemas import ok, server_error
from app.schemas.qa import QuestionRequest, AnswerResponse, QAHistoryResponse
from app.utils import ai_chat

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/qa", tags=["智能问答"])


@router.post("/ask")
async def ask_question(
        question_data: QuestionRequest,
        current_user_id: int = Depends(get_current_user_id),
        db = Depends(get_async_db)
):
    """
    提问接口
    """
    # 调用 LLM 模型进行问答
    try:
        # 1. 调用 AI API 获取回答
        answer = await ai_chat.call_ai_api(
            question=question_data.question,
            context=question_data.context
        )
        # 2. 保存问答记录
        qa_record = await qa.create_question(db, question_data.question, current_user_id,  answer ,question_data.context)
        # 3. 封装响应格式
        response_data = AnswerResponse(
            id = qa_record.id,
            question=question_data.question,
            answer=answer,
            user_id=qa_record.user_id,
            created_at=qa_record.created_at
        )

        logger.info(f"保存问答记录成功，ID: {qa_record.id}")
        return ok(data=response_data.model_dump(), message="提问成功")
    except Exception as e:
        logger.error(f"提问失败: {str(e)}")
        return server_error(message="提问失败")
@router.get("/history")
async def get_qa_history(
        current_user_id: int = Depends(get_current_user_id),
        db = Depends(get_async_db),
        limit : int = 50
):
    """
    获取问答历史记录
    """
    try:
        qa_records = await qa.get_user_qa_history(db, current_user_id, limit)
        response_data = [
            QAHistoryResponse(
                id=qa_record.id,
                question=qa_record.question,
                answer=qa_record.answer,
                created_at=qa_record.created_at
            ).model_dump() for qa_record in qa_records
        ]
        return ok(data=response_data, message="获取问答历史记录成功")
    except Exception as e:
        logger.error(f"获取问答历史记录失败: {str(e)}")
