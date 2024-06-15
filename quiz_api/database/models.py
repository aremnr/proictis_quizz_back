from sqlalchemy import ForeignKey, UUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
import datetime
import uuid


class QuizModel(Base):
    __tablename__ = "quizzes"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    dis: Mapped[str]
    owner_id: Mapped[str] = mapped_column(nullable=False)
    question_count: Mapped[int] = mapped_column(nullable=False)
    all_points: Mapped[int]
    create_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    questions_list = relationship("QuestionModel", back_populates="quiz")
    

class QuestionModel(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[str] = mapped_column(UUID, ForeignKey("quizzes.id", ondelete="CASCADE"))
    question_text: Mapped[str]
    points: Mapped[int]
    right_answer: Mapped[int] = mapped_column(nullable=False)
    pcl: Mapped[int] = mapped_column(nullable=False)
    quiz = relationship("QuizModel", back_populates="questions_list")
    answers = relationship("AnswerModel", back_populates="question")


class AnswerModel(Base):
    __tablename__ = "answers"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[str] = mapped_column(UUID, ForeignKey("questions.id", ondelete="CASCADE"))
    answer_text: Mapped[str]
    question = relationship("QuestionModel", back_populates="answers")

