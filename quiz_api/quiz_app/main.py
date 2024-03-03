from database.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
import quiz_app.crud as crud
import quiz_app.schemas as schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="test"
)

@app.post("/quiz/add")
def add(model: schemas.input_model, db: Session = Depends(get_db)):
    return crud.add_quiz(quiz=model.quiz, questions=model.qestions, db=db)
    
@app.get("/quiz/{quiz_id}", response_model=schemas.quiz)
def get_quiz_by_id(quiz_id: str, db: Session = Depends(get_db)):
    return crud.get_quiz(db=db, quiz_id=quiz_id)

@app.get("/quiz/{quiz_id}/question", response_model=schemas.question)
def get_question_of_quiz(quiz_id: str, question: int = 0, db: Session = Depends(get_db)):
    return crud.get_question(db=db, quiz_id=quiz_id, pcl=question)

@app.delete("/quiz/del/quiz", status_code=200)
def delete_quiz(*, quiz_id: str, db: Session = Depends(get_db)):
    return crud.delete_quiz(quiz_id=quiz_id, db=db)

@app.delete("/quiz/del/question", status_code=200)
def delete_question(*, question_id: str, db: Session = Depends(get_db)):
    return crud.delete_question(question_id=question_id, db=db)

@app.delete("/quiz/del/answer", status_code=200)
def delete_answer(*, answer_id: str, db: Session = Depends(get_db)):
    return crud.delete_answer(answer_id=answer_id, db=db)