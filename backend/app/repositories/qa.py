from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.qa_record import QARecord


# 新建提问
async def create_question(
        db: AsyncSession,
        question: str,
        user_id: int,
        answer: str,
        context: Optional[str] = None,
) -> QARecord:
    db_qa_record = QARecord(
        question=question,
        answer=answer,
        user_id=user_id,
        context=context,
        created_at = datetime.now()
    )
    db.add(db_qa_record)
    await db.commit()
    await db.refresh(db_qa_record)
    return db_qa_record


# 获取该用户历史提问记录
async def get_user_qa_history(db: AsyncSession,
                              user_id: int,
                              limit=50
                              ) -> List[QARecord]:
    result = await db.execute(
        select(QARecord).filter(
            QARecord.user_id == user_id
        ).order_by(
            QARecord.created_at.desc()
        ).limit(limit)
    )
    return result.scalars().all()
