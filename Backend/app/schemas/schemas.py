from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.models import VerdictEnum

class FactCheckBase(BaseModel):
    claim: str
    verdict: VerdictEnum
    explanation: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    category: Optional[str] = None

class FactCheckCreate(FactCheckBase):
    pass

class FactCheckResponse(FactCheckBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class QuizQuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    difficulty: str = "medium"
    points: int = 10

class QuizQuestionCreate(QuizQuestionBase):
    fact_check_id: int

class QuizQuestionResponse(QuizQuestionBase):
    id: int
    fact_check_id: int
    created_at: datetime

    class Config:
        from_attributes = True