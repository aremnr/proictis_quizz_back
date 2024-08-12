import uuid
from redis import Redis
import quiz_app.schemas as schemas


class RedisCache:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def check_in_cache(self, quiz_id: str | uuid.UUID = "", pcl: int = 0):
        quiz_id = str(quiz_id)
        if pcl == 0:
            return schemas.Quiz.parse_obj(self.redis_client.hgetall(f"{quiz_id}_{pcl}"))
        else:
            return self.redis_parse_to_question(self.redis_client.hgetall(f"{quiz_id}_{pcl}"))

    def add_to_cache(self, *, quiz: schemas.Quiz = None, question: schemas.Question = None):
        if not (quiz is None):
            quiz.dis = str(quiz.dis)
            quiz.id = str(quiz.id)
            self.redis_client.hset(f"{quiz.id}_0", mapping=dict(quiz))
            self.redis_client.expire(f"{quiz.id}_0", quiz.question_count*10*60)
        if not (question is None):
            question.id = str(question.id)
            question.quiz_id = str(question.quiz_id)
            rd_question = self.redis_parse_question(question)
            if self.add_answers(rd_question[1]):
                self.redis_client.set(f"{rd_question[0].id}", len(rd_question[1]))
                self.redis_client.hset(f"{rd_question[0].quiz_id}_{rd_question[0].pcl}", mapping=dict(rd_question[0]))
                self.redis_client.expire(f"{rd_question[0].quiz_id}_{rd_question[0].pcl}", 300)

    def add_answers(self, ans: list[dict]):
        for i, v in enumerate(ans):
            v["id"] = str(v["id"])
            v["question_id"] = str(v["question_id"])
            id = v['question_id']
            self.redis_client.hset(f"{id}_{i+1}", mapping=v)
            self.redis_client.expire(f"{id}_{i+1}", 300)
        return True

    def redis_parse_question(self, question: schemas.Question):
        result = [schemas.RdQuestion(
            id=question.id,
            quiz_id=question.quiz_id,
            question_text=question.question_text,
            points=question.points,
            right_answer=question.right_answer,
            pcl=question.pcl,
        )]
        answers = [
            dict(answer) for answer in question.answers_list.list
        ]
        result.append(answers)
        return result

    def redis_parse_to_question(self, rd_question: dict):
        id = rd_question['id']
        ans_count = int(self.redis_client.get(f"{id}"))
        answers = []
        for i in range(1, ans_count+1):
            ans = self.redis_client.hgetall(f"{id}_{i}")
            answers.append(schemas.Answer(id=ans["id"], question_id=ans["question_id"], answer_text=ans['answer_text']))
        answers = schemas.AnswerList(list=list(answers))
        result = schemas.Question(
            id=rd_question["id"],
            quiz_id=rd_question["quiz_id"],
            question_text=rd_question["question_text"],
            points=rd_question["points"],
            right_answer=rd_question["right_answer"],
            pcl=rd_question["pcl"],
            answers_list=answers
        )
        return result

    def add_cache(self, *, key: str, text: str, time: int = -1):
        self.redis_client.set(key, text)
        self.redis_client.expire(key, time)
        return True

    def check_cache(self, *, key: str):
        try:
            value = self.redis_client.get(key)
            return value
        except (...):
            return False