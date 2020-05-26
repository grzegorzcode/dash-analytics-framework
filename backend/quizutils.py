from werkzeug.security import check_password_hash
from backend.quizengine import *
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import and_, or_


def save_and_check_answer(quiz, questionid, answer, username):
    with session_scope() as s:
        s.query(Answers).filter(and_(Answers.user == username, Answers.questionid == questionid, Answers.quiz == quiz)).delete()
        answer = Answers(user=username, quiz=quiz, questionid=questionid, answer=answer, answerdate=datetime.now())
        s.add(answer)


def add_question():
    pass


def get_questions(quiz):
    with session_scope() as s:
        #questions = s.query(Questions).filter_by(quiz=quiz).all()
        return [question.__dict__ for question in s.query(Questions).filter_by(quiz=quiz).all()]
        # for u in s.query(Questions).filter_by(quiz=quiz).all():
        #     print(u.__dict__)


def get_questions_count(quiz):
    with session_scope() as s:
        return s.query(Questions).filter_by(quiz=quiz).count()


def get_next_question(quiz, questionid):
    with session_scope() as s:
        question = s.query(Questions.question, Questions.optiona, Questions.optionb, Questions.optionc, Questions.optiond).filter(and_(Questions.quiz == quiz, Questions.questionid == questionid)).first()
        return question


def del_question():
    pass



