from sqlalchemy import delete
from sqlalchemy.orm import Session
import database.models as models
import quiz_app.schemas as schemas
from pydantic import ValidationError
from cache.redis_main import cache


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


def add_question(db: Session, question: schemas.Question, quiz_id: str):
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


def add_answer(db: Session, answer: schemas.Answer, question_id: str):
    db_answer = models.AnswerModel(
        question_id=question_id,
        answer_text=answer.answer_text
    )
    db.add(db_answer)
    db.commit()


def add_quiz(db: Session, quiz: schemas.Quiz, questions: schemas.QuestionList):
    quiz_db = models.QuizModel(
        name=quiz.name,
        dis=quiz.dis,
        owner_id=quiz.owner_id,
        question_count=quiz.question_count,
        all_points=quiz.all_points
    )
    db.add(quiz_db)
    db.flush()
    add_question_list(db, questions, quiz_db.id)
    db.commit()


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
        question = db.query(models.QuestionModel).filter(models.QuestionModel.quiz_id == quiz_id).filter(models.QuestionModel.pcl == pcl).one()
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
        cache.add_to_cache(question=question)
        question.right_answer = -1
        return question


def delete_quiz(db: Session, quiz_id: str):
    query = (
        delete(models.QuizModel)
        .filter(models.QuizModel.id == quiz_id)
    )
    db.execute(query)
    db.commit()


def delete_question(db: Session, question_id: str):
    query = (
        delete(models.QuestionModel)
        .filter(models.QuestionModel.id == question_id)
    )
    db.execute(query)
    db.commit()


def delete_answer(db: Session, answer_id: str):
    query = (
        delete(models.AnswerModel)
        .filter(models.AnswerModel.id == answer_id)
    )
    db.execute(query)
    db.commit()


def check_answer(db: Session, quiz_id: str, pcl: int, answer_plc: int):
    try:
        right_answer: int = cache.check_in_cache(quiz_id=quiz_id, pcl=pcl).right_answer
    except KeyError:
        right_answer: int = (
            db.query(models.QuestionModel).filter(models.QuestionModel.quiz_id == quiz_id)
            .filter(models.QuestionModel.pcl == pcl)
            .one()).right_answer

    print(right_answer)
    print(answer_plc)
    return schemas.Check(is_right=(right_answer == answer_plc))
