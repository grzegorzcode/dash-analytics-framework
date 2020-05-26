from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, FLOAT, Integer, TIMESTAMP, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


engine = create_engine('sqlite:///backend/internal.db')
#engine = create_engine('sqlite:///internal.db')

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


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(32))
    password = Column(VARCHAR(100))
    admin = Column(VARCHAR(1))
    created = Column(TIMESTAMP)


class UsersLogins(Base):
    __tablename__ = "userslogins"
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(32))
    event = Column(VARCHAR(32))
    eventtime = Column(TIMESTAMP)
    sessionid = Column(VARCHAR(100))
