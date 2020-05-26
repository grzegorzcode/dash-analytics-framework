from werkzeug.security import check_password_hash
from backend.dbengine import *
from datetime import datetime
from werkzeug.security import generate_password_hash


def check_password(user, password):
    with session_scope() as s:
        user = s.query(Users).filter_by(username=user).first()
        if user:
            if check_password_hash(user.password, password):
                return True
            else:
                return False


def check_admin(user):
    with session_scope() as s:
        user = s.query(Users).filter_by(username=user).first()
        if user.admin == 'Y':
            return True
        else:
            return False


def add_user(username, password, admin):
    with session_scope() as s:
        newuser = Users(username=username, password=generate_password_hash(password, method='sha256'), admin=admin, created=datetime.now())
        s.add(newuser)
        return True


def show_users():
    with session_scope() as s:
        users = s.query(Users.username, Users.admin).all()
        return users


def del_user(username):
    with session_scope() as s:
        user = s.query(Users).filter_by(username=username).delete()
        return bool(user)


def user_exists(user):
    with session_scope() as s:
        user = s.query(Users).filter_by(username=user).count()
        return bool(user)


def change_password(username, newpassword):
    if not user_exists(username):
        return False
    hashed_password = generate_password_hash(newpassword, method='sha256')
    with session_scope() as s:
        statement = s.query(Users).filter_by(username=username).update({"password": hashed_password})
        return bool(statement)


def add_user_session_info(username, event, sessionid, level=1):
    TRACELEVEL = 2  # TODO: move this to config file
    if level <= TRACELEVEL:
        with session_scope() as s:
            if sessionid:
                newevent = UsersLogins(username=username, event=event, eventtime=datetime.now(), sessionid=sessionid)
                s.add(newevent)
                return True
            else:
                return False
    else:
        return False


def change_user(first,last,email,engine):
    #not implemented
    pass


def send_password_key(email,firstname,engine):
    # not implemented
    pass


def validate_password_key(email, key, engine):
    # not implemented
    pass


