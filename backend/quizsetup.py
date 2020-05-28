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
        answer = Useranswers(user='gc', quiz='GEO', questionid=1, answer='C')
        s.add(answer)
        answer = Useranswers(user='gc', quiz='GEO', questionid=2, answer='C')
        s.add(answer)
        answer = Useranswers(user='gc', quiz='GEO', questionid=3, answer='C')
        s.add(answer)


if __name__ == '__main__':
    recreate_database()
    recreate_initial_quiz()



