from sqlalchemy import delete
from sqlalchemy.orm import Session
import quiz_app.models as models
import quiz_app.schemas as schemas
from pydantic import ValidationError
from cache.redis_main import cache



def get_quiz(db: Session, quiz_id: str):
    try:
        assert cache.check_in_cache(quiz_id=quiz_id)
        return cache.check_in_cache(quiz_id=quiz_id)
    except (KeyError, ValidationError):
        print("Hello From Postgres")
        quiz = schemas.Quiz.model_validate(
            db.query(models.QuizModel).filter(models.QuizModel.id == quiz_id).one(), from_attributes=True
        )
        cache.add_to_cache(quiz=quiz)
        return quiz


def get_question(db: Session, quiz_id: str, pcl: int):
    try:
        return cache.check_in_cache(quiz_id=quiz_id, pcl=pcl)
    except KeyError:
        print("Hello From Postgres")
        question = db.query(models.QuestionModel).filter(models.QuestionModel.quiz_id == quiz_id).filter(
            models.QuestionModel.pcl == pcl).one()
        answers = schemas.AnswerList(list=[
            schemas.Answer.model_validate(answer) for answer in question.answers
        ])
        question = schemas.Question(
            id=question.id,
            quiz_id=question.quiz_id,
            question_text=question.question_text,
            points=question.points,
            right_answer=question.right_answer,
            pcl=question.pcl,
            answers_list=answers
        )
        question.right_answer = -1
        cache.add_to_cache(question=question)
        return question


def add_answer_list(db: Session, answer_list: schemas.AnswerList, question_id: str):
    for answer in answer_list.list:
        db_answer = models.AnswerModel(
            question_id=question_id,
            answer_text=answer.answer_text
        )
        db.add(db_answer)
        db.flush()


def add_question_list(db: Session, question_list: schemas.QuestionList, quiz_id: str):
    for question in question_list.list:
        db_question = models.QuestionModel(
            quiz_id=quiz_id,
            question_text=question.question_text,
            points=question.points,
            right_answer=question.right_answer,
            pcl=question.pcl
        )
        db.add(db_question)
        db.flush()
        add_answer_list(db=db, answer_list=question.answers_list, question_id=db_question.id)


def add_question(db: Session, question: schemas.Question, quiz_id: str, admin_id: str):
    if get_quiz(db=db, quiz_id=quiz_id).owner_id == str(admin_id):
        db_question = models.QuestionModel(
            quiz_id=quiz_id,
            question_text=question.question_text,
            points=question.points,
            right_answer=question.right_answer,
            pcl=question.pcl
        )
        db.add(db_question)
        db.flush()
        add_answer_list(db=db, answer_list=question.answers_list, question_id=db_question.id)
        db.commit()
    else:
        return {"message": "You are not the creator of this quiz"}


def add_answer(db: Session, answer: schemas.Answer, quiz_id: str, pcl: int, admin_id: str):
    if get_quiz(db=db, quiz_id=quiz_id).owner_id == str(admin_id):
        question_id = get_question(db=db, quiz_id=quiz_id, pcl=pcl).id
        db_answer = models.AnswerModel(
            question_id=question_id,
            answer_text=answer.answer_text
        )
        db.add(db_answer)
        db.commit()
    else:
        return {"message": "You are not the creator of this quiz"}

def add_quiz(db: Session, quiz: schemas.Quiz, questions: schemas.QuestionList, owner_id: str):
    quiz_db = models.QuizModel(
        name=quiz.name,
        dis=quiz.dis,
        owner_id=owner_id,
        question_count=quiz.question_count,
        all_points=quiz.all_points
    )
    db.add(quiz_db)
    db.flush()
    add_question_list(db, questions, quiz_db.id)
    db.commit()


def delete_quiz(db: Session, quiz_id: str, admin_id: str):
    if get_quiz(db=db, quiz_id=quiz_id).owner_id == str(admin_id):
        query = (
            delete(models.QuizModel)
            .filter(models.QuizModel.id == quiz_id)
        )
        db.execute(query)
        db.commit()
    else:
        return {"message": "You are not the creator of this quiz"}

def delete_question(db: Session, quiz_id: str, pcl: int, admin_id: str):
    if get_quiz(db=db, quiz_id=quiz_id).owner_id == str(admin_id):
        question_id =  get_question(db=db, quiz_id=quiz_id, pcl=pcl).id
        query = (
            delete(models.QuestionModel)
            .filter(models.QuestionModel.id == question_id)
        )
        db.execute(query)
        db.commit()
    else:
        return {"message": "You are not the creator of this quiz"}

def delete_answer(db: Session, answer_id: str):
    query = (
        delete(models.AnswerModel)
        .filter(models.AnswerModel.id == answer_id)
    )
    db.execute(query)
    db.commit()


def check_answer(db: Session, quiz_id: str, pcl: int, answer_plc: int):
    right_answer: int = (
        db.query(models.QuestionModel).filter(models.QuestionModel.quiz_id == quiz_id)
        .filter(models.QuestionModel.pcl == pcl)
        .one()).right_answer
    return schemas.Check(is_right=(right_answer == answer_plc))


def get_right_answer(db: Session, quiz_id: str, pcl: int):
    question = db.query(models.QuestionModel).filter(models.QuestionModel.quiz_id == quiz_id).filter(
        models.QuestionModel.pcl == pcl).one()
    return str(question.answers[question.right_answer-1].answer_text)
