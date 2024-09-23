import quiz_app.crud as crud
import quiz_app.schemas as schemas
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from database.database import get_db
from admin_side.admin_func import get_current_admin
from admin_side.schemas import AdminSchema
from typing import Annotated
router = APIRouter()


@router.post("/quiz/add", tags=["quiz"])
def add(model: schemas.InputQuiz, admin: Annotated[AdminSchema, Depends(get_current_admin)], db: Session = Depends(get_db)):
    model = crud.model_valid(model)
    return crud.add_quiz(quiz=model.quiz, questions=model.questions, db=db, owner_id=admin.id)


@router.post("/quiz/{quiz_id}/add/question", tags=["quiz"])
def add_question(model: schemas.Question, quiz_id: str, admin: Annotated[AdminSchema, Depends(get_current_admin)], db: Session = Depends(get_db)):
    return crud.add_question(db=db, question=model, quiz_id=quiz_id, admin_id=admin.id)


@router.post("/quiz/{quiz_id}/{pcl}/add", tags=["quiz"])
def add_answer(quiz_id: str,pcl:int, model: schemas.Answer, admin: Annotated[AdminSchema, Depends(get_current_admin)], db: Session = Depends(get_db)):
    return crud.add_answer(db=db, answer=model, quiz_id=quiz_id,pcl=pcl, admin_id=admin.id)


@router.get("/quiz/{quiz_id}", response_model=schemas.Quiz, tags=["quiz"])
def get_quiz_by_id(quiz_id: str, db: Session = Depends(get_db)):
    return crud.get_quiz(db=db, quiz_id=quiz_id)


@router.get("/quiz/{quiz_id}/question", response_model=schemas.Question, tags=["quiz"])
def get_question_of_quiz(quiz_id: str, question_number: int = 0, db: Session = Depends(get_db)):
    return crud.get_question(db=db, quiz_id=quiz_id, pcl=question_number)


@router.delete("/quiz/del/{quiz_id}", status_code=200, tags=["quiz"])
def delete_quiz(*, quiz_id: str, admin: Annotated[AdminSchema, Depends(get_current_admin)], db: Session = Depends(get_db)):
    return crud.delete_quiz(quiz_id=quiz_id, db=db, admin_id=admin.id)


@router.delete("/quiz/del/{quiz_id}/{pcl}", status_code=200, tags=["quiz"])
def delete_question(*, quiz_id: str, pcl: int,  admin: Annotated[AdminSchema, Depends(get_current_admin)], db: Session = Depends(get_db)):
    return crud.delete_question(quiz_id=quiz_id,pcl=pcl,admin_id=admin.id, db=db)


@router.delete("/quiz/del/{answer_id}", status_code=200, tags=["quiz"])
def delete_answer(*, answer_id: str, admin: Annotated[AdminSchema, Depends(get_current_admin)], db: Session = Depends(get_db)):
    return crud.delete_answer(answer_id=answer_id, db=db)


@router.get("/quiz/{quiz_id}/ans_check", response_model=schemas.Check, tags=["quiz"])
def check_answer(quiz_id: str, admin: Annotated[AdminSchema, Depends(get_current_admin)], *, question_number: int = 1, answer_number: int = 0, db: Session = Depends(get_db)):
    return crud.check_answer(db=db, quiz_id=quiz_id, pcl=question_number, answer_plc=answer_number)


@router.get("/temp")
def get_all_quizzes_by_owner_id(admin: Annotated[AdminSchema, Depends(get_current_admin)], db: Session = Depends(get_db)):
    return {"quizzes": crud.get_quiz_by_own_id(db=db, owner_id=str(admin.id))}

