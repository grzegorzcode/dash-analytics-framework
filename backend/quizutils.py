from werkzeug.security import check_password_hash
from backend.quizengine import *
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import and_, or_
import pandas as pd


def save_and_check_answer(quiz, questionid, answer, username):
    with session_scope() as s:
        s.query(Useranswers).filter(and_(Useranswers.user == username, Useranswers.questionid == questionid, Useranswers.quiz == quiz)).delete()
        answer = Useranswers(user=username, quiz=quiz, questionid=questionid, answer=answer, answerdate=datetime.now())
        s.add(answer)
        s.commit()


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


def get_answers(quiz, username):
    # with engine.connect() as s:
    #     res = pd.read_sql("select * from useranswers", con=s)
    #     return res
    with engine.connect() as s:
        stmt = pd.read_sql(f"""
        select a.user, a.quiz, a.questionid, a.answer, q.correctanswer,
        case
            when a.answer = q.correctanswer
                then 'Y'
            when a.answer != q.correctanswer
                then 'N'
        end ISCORRECT
        from useranswers a, questions q
        where a.quiz = q.quiz and a.questionid = q.questionid and a.quiz = '{quiz}' and a.user = '{username}'""", con=s)
        # rs = s.execute(stmt)
        # return [row for row in rs]
        return stmt


def get_all_users_answered(quiz):
    with session_scope() as s:
        users = s.query(Useranswers.user).distinct(Useranswers.user).all()
        return [x[0] for x in users]




