from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, Boolean, UUID
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()
metadata = Base.metadata

class Quiz(Base):
    __tablename__ = "quizzes"
    
    
    id = Column(UUID, primary_key=True)
    quiz_description = Column(String)
    questin_count = Column(Integer)
    ball = Column(Integer)


class Question(Base):
    __tablename__ = "questions"
    

    id = Column(UUID, primary_key=True)
    quiz_id = Column(UUID, ForeignKey("quizzes.id"))
    question = Column(String, index=True)

class Answer(Base):
    __tablename__ = "answers"
    

    id = Column(UUID, primary_key=True)
    question_id = Column(UUID, ForeignKey("questions.id"))
    answer = Column(String, index=True)
    
    