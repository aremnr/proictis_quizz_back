from sqlalchemy import delete, select
from sqlalchemy.orm import Session
import database.models as models
import quiz_app.schemas as schemas

def add_answer_list(db: Session, answer_list: schemas.answer_list, question_id: str):
    for answer in answer_list.list :
        db_answer = models.Answer(
            question_id=question_id,
            answer_text=answer.answer_text
            )
        db.add(db_answer)
        db.flush()
    

def add_question_list(db: Session, question_list: schemas.question_list, quiz_id: str):
    for question in question_list.list:
        db_question = models.Question(
            quiz_id=quiz_id,
            question_text=question.question_text,
            points = question.points,
            right_answer = question.right_answer,
            pcl = question.pcl
            )
        db.add(db_question)
        db.flush()
        add_answer_list(db=db, answer_list=question.answers_list, question_id=db_question.id)


def add_quiz(db:Session, quiz: schemas.quiz, questions: schemas.question_list):
    quiz_db = models.Quiz(
        name = quiz.name, 
        dis = quiz.dis,
        owner_id = quiz.owner_id,
        question_count = quiz.question_count,
        all_points = quiz.all_points
        )
    db.add(quiz_db)
    db.flush()
    add_question_list(db, questions, quiz_db.id)
    db.commit()


def get_quiz(db: Session, quiz_id: str):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).one()

def get_question(db: Session, quiz_id: str, pcl: int):
    question = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).filter(models.Question.pcl == pcl).one()
    answers = schemas.answer_list(list=[
         schemas.answer.model_validate(answer) for answer in question.answers
     ])
    question = schemas.question.model_validate(question)
    question.answers_list = answers
    return question

def delete_quiz(db: Session, quiz_id: str):
    query = (
        delete(models.Quiz)
        .filter(models.Quiz.id == quiz_id)
    )
    db.execute(query)
    db.commit()

def delete_question(db: Session, question_id: str):
    query = (
        delete(models.Question)
        .filter(models.Question.id == question_id)
    )
    db.execute(query)
    db.commit()

def delete_answer(db: Session, answer_id: str):
    query = (
        delete(models.Answer)
        .filter(models.Answer.id == answer_id)
    )
    db.execute(query)
    db.commit()
