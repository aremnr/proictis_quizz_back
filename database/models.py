from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from .database import Base

metadata = Base.metadata

class Quiz(Base):
    __tablename__ = "quizzes"
    
    
    id = Column(UUID, primary_key=True)
    quiz_name = Column(String, index=True)
    quiz_description = Column(String)
    questin_count = Column(Integer)
    ball = Column(Integer)
    questions_list = relationship("Question", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"
    

    id = Column(UUID, primary_key=True)
    quiz_id = Column(UUID, ForeignKey("quizzes.id"))
    question_text = Column(String)
    quiz = relationship("Quiz", back_populates="questions_list")
    answers_list = relationship("Answer", back_populates="question") 

class Answer(Base):
    __tablename__ = "answers"
    

    id = Column(UUID, primary_key=True)
    question_id = Column(UUID, ForeignKey("questions.id"))
    answer_text = Column(String)
    question = relationship("Question", back_populates="answers_list")
    
    