from datetime import datetime
from werkzeug.security import generate_password_hash
from backend.quizengine import *


def recreate_database():
    engine.connect()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def recreate_initial_quiz():
    with session_scope() as s:
        question = Questions(quiz='GEO', question='location of krakow', questionid=1, optiona='usa', optionb='uk', optionc='pl', optiond='ru', correctanswer='C')
        s.add(question)
        question = Questions(quiz='GEO', question='homeland of harley', questionid=2, optiona='jp', optionb='usa', optionc='cz', optiond='sk', correctanswer='B')
        s.add(question)
        question = Questions(quiz='GEO', question='where are you now', questionid=3, optiona='earth', optionb='jupyter', optionc='nubiru', optiond='moon', correctanswer='A')
        s.add(question)


recreate_database()
recreate_initial_quiz()



