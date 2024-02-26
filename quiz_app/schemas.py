from pydantic import BaseModel

class question(BaseModel):
    question: str
    answers: dict[int: str]
    ball: int | None
    right: int


class quiz(BaseModel):
    name: str
    discrition: str
    questionCount: int
    balls: int | None
    questions: list[question]


