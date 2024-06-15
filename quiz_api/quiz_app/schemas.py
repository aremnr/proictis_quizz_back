from pydantic import BaseModel, ConfigDict
import uuid


class Answer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | uuid.UUID
    question_id: str | uuid.UUID
    answer_text: str


class AnswerList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    list: list[Answer]


class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | uuid.UUID
    quiz_id: str | uuid.UUID
    question_text: str | None
    points: int
    right_answer: int | None
    pcl: int | None
    answers_list: AnswerList


class QuestionList(BaseModel):
    list: list[Question]


class Quiz(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | uuid.UUID
    name: str
    dis: str | None
    question_count: int
    owner_id: str
    all_points: int
    
    
class InputModel(BaseModel):
    quiz: Quiz
    questions: QuestionList


class RdQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str | uuid.UUID
    quiz_id: str | uuid.UUID
    question_text: str
    points: int
    right_answer: int
    pcl: int


class Check(BaseModel):
    is_right: bool


class Admin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str | uuid.UUID
    username: str | None
    email: str | None
    password: str | None
    is_admin: bool = True


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str | None


class AdminValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    #JWT: str | None
    is_admin: bool
