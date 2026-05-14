from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class VerdictEnum(str, enum.Enum):
    TRUE = "true"
    FALSE = "false"
    MISLEADING = "misleading"
    PARTIALLY_TRUE = "partially_true"
    UNVERIFIED = "unverified"

class FactCheck(Base):
    __tablename__ = "fact_checks"
    id = Column(Integer, primary_key=True, index=True)
    claim = Column(Text, nullable=False)
    verdict = Column(Enum(VerdictEnum), nullable=False)
    explanation = Column(Text)
    source_url = Column(String(500))
    source_name = Column(String(200))
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    quiz_questions = relationship("QuizQuestion", back_populates="fact_check")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True, index=True)
    fact_check_id = Column(Integer, ForeignKey("fact_checks.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(String(300))
    option_b = Column(String(300))
    option_c = Column(String(300))
    option_d = Column(String(300))
    correct_option = Column(String(1), nullable=False)
    difficulty = Column(String(20), default="medium")
    points = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fact_check = relationship("FactCheck", back_populates="quiz_questions")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    total_score = Column(Integer, default=0)
    games_played = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    game_results = relationship("GameResult", back_populates="user")

class GameResult(Base):
    __tablename__ = "game_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, default=0)
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    time_taken_seconds = Column(Integer)
    played_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="game_results")