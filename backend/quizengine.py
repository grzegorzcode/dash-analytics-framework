from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, FLOAT, Integer, TIMESTAMP, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


engine = create_engine('sqlite:///backend/quiz.db')


Session = sessionmaker(bind=engine)
# PREPARING DATABASE
Base = declarative_base()


# PREPARE SESSION CONTEXT
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Questions(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    quiz = Column(VARCHAR(100))
    question = Column(VARCHAR(1))
    questionid = Column(Integer)
    optiona = Column(VARCHAR(40))
    optionb = Column(VARCHAR(40))
    optionc = Column(VARCHAR(40))
    optiond = Column(VARCHAR(40))
    correctanswer = Column(VARCHAR(1))


class Answers(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    user = Column(VARCHAR(100))
    quiz = Column(VARCHAR(100))
    questionid = Column(VARCHAR(1))
    answer = Column(VARCHAR(1))
    answerdate = Column(TIMESTAMP)

