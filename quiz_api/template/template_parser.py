from fastapi import Request
from fastapi.templating import Jinja2Templates
import quiz_app.crud as crud
import quiz_app.schemas as schemas
templates = Jinja2Templates(directory="template")


def get_html_response(request: Request, quiz_id: str, db,  pcl: int = 1):
    quiz: schemas.Quiz = crud.get_quiz(quiz_id=quiz_id, db=db)
    question: schemas.Question = crud.get_question(quiz_id=quiz_id, db=db, pcl=pcl)
    return templates.TemplateResponse(request=request, name="index.html", context={
        "quiz_name": quiz.name,
        "question": question.question_text,
        "answer_1": question.answers_list.list[0].answer_text,
        "answer_2": question.answers_list.list[1].answer_text,
        "answer_3": question.answers_list.list[2].answer_text,
        "answer_4": question.answers_list.list[3].answer_text
    })
