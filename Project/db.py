"""
 Implements a simple database of users.

"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Date, Boolean
from sqlalchemy.schema import ForeignKey
from datetime import datetime, timedelta

Base = declarative_base()


def as_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    creation_date = Column(Date)
    last_updated = Column(Date)

    user = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __init__(self, title, creation_date, last_updated, user_id):
        self.title = title
        self.creation_date = creation_date
        self.last_updated = last_updated
        self.user = user_id


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    order = Column(Integer)
    creation_date = Column(Date)
    due_date = Column(Date)
    completed = Column(Boolean)

    project = Column(Integer, ForeignKey("projects.id"), nullable=False)

    def __init__(self, title, order, creation_date, due_date, completed, project_id):
        self.title = title
        self.order = order
        self.creation_date = creation_date
        self.due_date = due_date
        self.completed = completed
        self.project = project_id


engine = create_engine('sqlite:///user.db')
Base.metadata.create_all(engine)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def recreate_db():
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())
    session = DBSession()
    ana = User('Ana', "anocas", "anocas@gmail.com", "123")
    paulo = User('Paulo', "paulocas", "paulinho@yahoo.com", "123")

    project1 = Project("first project", datetime.now(), datetime.now(), 1)
    due_date = datetime.now() + timedelta(days=2)
    task1 = Task("task1", 1, datetime.now(), due_date, False, 1)

    session.add(ana)
    session.add(paulo)
    session.add(project1)
    session.add(task1)

    session.commit()
    session.close()


def get_users():
    session = DBSession()
    res = session.query(User).all()
    res_list = []
    for user in res:
        res_list.append(as_dict(user))

    session.close()
    return res_list


def get_user(pk):
    session = DBSession()
    res = session.query(User).get(pk)

    user = as_dict(res)
    session.close()
    return user


def add_user(user):
    session = DBSession()
    user = User(user['name'], user['username'], user['email'], user['password'])

    session.add(user)
    session.commit()

    dic = as_dict(user)
    session.close()

    return dic


def update_user(user, data):
    session = DBSession()
    u = session.query(User).get(user['id'])
    if data['name'] is not "":
        u.name = data['name']
    if data['username'] is not "":
        u.username = data['username']
    if data['email'] is not "":
        u.email = data['email']
    if data['password'] is not "":
        u.password = data['password']

    session.commit()

    user_id = u.id
    session.close()
    return get_user(user_id)


def remove_user(user):
    session = DBSession()
    u = session.query(User).get(user['id'])
    session.delete(u)

    session.commit()
    session.close()


def get_projects():
    session = DBSession()
    res = session.query(Project).all()
    res_list = []
    for project in res:
        res_list.append(as_dict(project))

    session.close()
    return res_list
