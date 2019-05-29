"""
 Implements a simple database of users.

"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.schema import ForeignKey
from datetime import datetime, timedelta

Base = declarative_base()


def as_dict(obj):
    if obj is None:
        return {}
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
    creation_date = Column(DateTime)
    last_updated = Column(DateTime)

    user = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __init__(self, title, user_id):
        self.title = title
        self.creation_date = datetime.now()
        self.last_updated = datetime.now()
        self.user = user_id


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    order = Column(Integer)
    creation_date = Column(DateTime)
    due_date = Column(DateTime)
    completed = Column(Boolean)

    project = Column(Integer, ForeignKey("projects.id"), nullable=False)

    def __init__(self, title, order, due_date, completed, project_id):
        self.title = title
        self.order = order
        self.creation_date = datetime.now()
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

    project1 = Project("first project", 1)
    project2 = Project("second project", 2)
    due_date = datetime.now() + timedelta(days=2)
    task1 = Task("task1", 1, due_date, False, 1)

    session.add(ana)
    session.add(paulo)
    session.add(project1)
    session.add(project2)
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
    user_obj = User(user['name'], user['username'], user['email'], user['password'])

    session.add(user_obj)
    session.commit()

    dic = as_dict(user_obj)
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


def get_project(pk):
    session = DBSession()
    res = session.query(Project).get(pk)

    project = as_dict(res)
    session.close()
    return project


def get_projects_of_user(user_pk):
    session = DBSession()
    res = session.query(Project).join(User).filter(User.id == user_pk)

    res_list = []
    for project in res:
        res_list.append(as_dict(project))

    session.close()
    return res_list


def add_project(project):
    session = DBSession()
    project_obj = Project(project['title'], project['user'])

    session.add(project_obj)
    session.commit()

    dic = as_dict(project_obj)
    session.close()

    return dic


def update_project(project, data):
    session = DBSession()
    p = session.query(User).get(project['id'])
    if data['title'] is not "":
        p.title = data['title']
    if data['creation_date'] is not "":
        p.creation_date = data['creation_date']
    if data['last_updated'] is not "":
        p.last_updated = data['last_updated']
    if data['user'] is not "":
        p.user = data['user']

    session.commit()

    project_id = p.id
    session.close()
    return get_project(project_id)


def remove_project(project):
    session = DBSession()
    p = session.query(Project).get(project['id'])
    session.delete(p)

    session.commit()
    session.close()


def get_tasks(project_pk):
    session = DBSession()
    res = session.query(Task).join(Project).filter(Project.id == project_pk)
    res_list = []
    for task in res:
        res_list.append(as_dict(task))

    session.close()
    return res_list


def get_task(project_pk, pk):
    session = DBSession()
    res = session.query(Task).join(Project).filter(Project.id == project_pk).filter(Task.id == pk)
    res_list = []
    for task in res:
        res_list.append(as_dict(task))

    session.close()
    return res_list


def add_task(task):
    session = DBSession()
    task_obj = Task(task['title'], task['order'], task['due_date'], task['completed'],
                    task['project'])

    session.add(task_obj)
    session.commit()

    dic = as_dict(task_obj)
    session.close()

    return dic


def update_task(task, data):
    session = DBSession()
    t = session.query(User).get(task['id'])
    if data['title'] is not "":
        t.title = data['title']
    if data['order'] is not "":
        t.order = data['order']
    if data['creation_date'] is not "":
        t.creation_date = data['creation_date']
    if data['due_date'] is not "":
        t.due_date = data['due_date']
    if data['completed'] is not "":
        t.completed = data['completed']
    if data['project'] is not "":
        t.project = data['project']

    session.commit()

    task_id = t.id
    session.close()
    return get_user(task_id)


def remove_task(task):
    session = DBSession()
    t = session.query(Task).get(task['id'])
    session.delete(t)

    session.commit()
    session.close()
