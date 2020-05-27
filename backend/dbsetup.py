from datetime import datetime
from werkzeug.security import generate_password_hash
from backend.dbengine import *


def recreate_database():
    engine.connect()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def recreate_initial_users():
    with session_scope() as s:
        adminuser = Users(username='gcadmin', password=generate_password_hash('gcadminpass', method='sha256'), admin='Y', created=datetime.now())
        s.add(adminuser)
        normaluser = Users(username='gc', password=generate_password_hash('gcpass', method='sha256'), admin='N', created=datetime.now())
        s.add(normaluser)


if __name__ == '__main__':
    recreate_database()
    recreate_initial_users()
