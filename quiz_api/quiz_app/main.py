from database.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Request
import quiz_app.crud as crud
import quiz_app.schemas as schemas
from fastapi.responses import HTMLResponse
from template.template_parser import get_html_response
from fastapi.staticfiles import StaticFiles


def get_db():
    db = SessionLocal()
    try:
        db.expire_all()
        yield db
    finally:
        db.close()


app = FastAPI(
    title="test"
)


@app.post("/quiz/add")
def add(model: schemas.InputModel, db: Session = Depends(get_db)):
    return crud.add_quiz(quiz=model.quiz, questions=model.questions, db=db)


@app.post("/quiz/{quiz_id}/add/question")
def add_question(model: schemas.Question, quiz_id: str, db: Session = Depends(get_db)):
    return crud.add_question(db=db, question=model, quiz_id=quiz_id)


@app.post("/quiz/{quiz_id}/{question_id}/add")
def add_answer(quiz_id: str, question_id: str, model: schemas.Answer, db: Session = Depends(get_db)):
    return crud.add_answer(db=db, answer=model, question_id=question_id)


@app.get("/quiz/{quiz_id}", response_model=schemas.Quiz)
def get_quiz_by_id(quiz_id: str, db: Session = Depends(get_db)):
    return crud.get_quiz(db=db, quiz_id=quiz_id)


@app.get("/quiz/{quiz_id}/question", response_model=schemas.Question)
def get_question_of_quiz(quiz_id: str, question_number: int = 0, db: Session = Depends(get_db)):
    return crud.get_question(db=db, quiz_id=quiz_id, pcl=question_number)


@app.delete("/quiz/del/quiz/{quiz_id}", status_code=200)
def delete_quiz(*, quiz_id: str, db: Session = Depends(get_db)):
    return crud.delete_quiz(quiz_id=quiz_id, db=db)


@app.delete("/quiz/del/question/{question_id}", status_code=200)
def delete_question(*, question_id: str, db: Session = Depends(get_db)):
    return crud.delete_question(question_id=question_id, db=db)


@app.delete("/quiz/del/answer/{answer_id}", status_code=200)
def delete_answer(*, answer_id: str, db: Session = Depends(get_db)):
    return crud.delete_answer(answer_id=answer_id, db=db)


@app.get("/quiz/{quiz_id}/ans_check", response_model=schemas.Check)
def check_answer(quiz_id: str, *, question_number: int = 1, answer_number: int = 0, db: Session = Depends(get_db)):
    return crud.check_answer(db=db, quiz_id=quiz_id, pcl=question_number, answer_plc=answer_number)


app.mount("/static", StaticFiles(directory="template/static"), name="static")


@app.get("/get_html/{quiz_id}/{pcl}", response_class=HTMLResponse)
def get_html(request: Request, quiz_id: str, pcl: int, db:Session = Depends(get_db)):
    return get_html_response(request=request, quiz_id=quiz_id, db=db, pcl=pcl)

