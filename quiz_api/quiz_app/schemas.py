from pydantic import BaseModel, ConfigDict
import uuid


class answer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | uuid.UUID
    question_id: str | uuid.UUID
    answer_text: str

class answer_list(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    list: list[answer]

class question(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | uuid.UUID
    quiz_id: str | uuid.UUID
    question_text: str | None
    points: int
    right_answer: int | None
    pcl: int | None
    answers_list: answer_list = []

class question_list(BaseModel):
    list: list[question]

class quiz(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    
    id: str | uuid.UUID
    name: str
    dis: str | None
    question_count: int
    owner_id: str
    all_points: int
    
    
class input_model(BaseModel):
    quiz: quiz
    qestions: question_list
