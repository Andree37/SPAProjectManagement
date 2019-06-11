"""
 Implements a simple database of users.

"""
from datetime import timedelta

from sqlalchemy import exc
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    def __init__(self, name="", username="", email="", password=""):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    creation_date = Column(DateTime)
    last_updated = Column(DateTime)

    user = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_ref = relationship('User', backref="Project")

    def __init__(self, title="", user_id=0):
        self.title = title
        self.creation_date = datetime.now()
        self.last_updated = datetime.now()
        self.user = user_id

    def __repr__(self):
        return '<Project %r>' % self.title


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    order = Column(Integer, autoincrement=True)
    creation_date = Column(DateTime)
    due_date = Column(DateTime)
    completed = Column(Boolean)

    project = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project_ref = relationship('Project', backref="Task")

    def __init__(self, title="", order=0, due_date=datetime.now(), completed=False, project_id=0):
        self.title = title
        self.order = order
        self.creation_date = datetime.now()
        self.due_date = due_date
        self.completed = completed
        self.project = project_id

    def __repr__(self):
        return '<Task %r>' % self.title


def as_dict(obj):
    if obj is None:
        return {}
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DataBase:

    def __init__(self, app):
        self.db = SQLAlchemy(app)

        # admin for all the tables
        admin = Admin(app)
        admin.add_view(ModelView(User, self.db.session))
        admin.add_view(ModelView(Project, self.db.session))
        admin.add_view(ModelView(Task, self.db.session))

    def recreate_db(self):
        meta = self.db.metadata
        for table in reversed(meta.sorted_tables):
            self.db.session.execute(table.delete())
        self.db.session.commit()

        ana = User('Ana', "anocas", "anocas@gmail.com", "123")
        paulo = User('Paulo', "paulocas", "paulinho@yahoo.com", "123")

        project1 = Project("first project", 1)
        project2 = Project("second project", 2)
        due_date = datetime.now() + timedelta(days=2)
        task1 = Task("task1", 1, due_date, False, 1)
        task2 = Task("task2", 1, due_date, False, 2)

        self.db.session.add(ana)
        self.db.session.add(paulo)
        self.db.session.add(project1)
        self.db.session.add(project2)
        self.db.session.add(task1)
        self.db.session.add(task2)

        self.db.session.commit()

    def get_users(self):
        res = self.db.session.query(User).all()
        res_list = []
        for user in res:
            res_list.append(as_dict(user))

        return res_list

    def get_user(self, pk):
        res = self.db.session.query(User).get(pk)

        user = as_dict(res)
        return user

    def get_user_load(self, pk):
        res = self.db.session.query(User).get(pk)

        return res

    def get_user_login(self, username, password):
        res = self.db.session.query(User).filter_by(username=username, password=password).first()
        return res

    def add_user(self, user):
        name = ""
        username = ""
        email = ""
        password = ""

        if user is None:
            return None

        if 'name' in user:
            name = user['name']
        if 'username' in user:
            username = user['username']
        if 'email' in user:
            email = user['email']
        if 'password' in user:
            password = user['password']

        if name == "" or username == "" or email == "" or password == "":
            return None
        user_obj = User(name, username, email, password)

        self.db.session.add(user_obj)
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return None

        dic = as_dict(user_obj)

        return dic

    def update_user(self, user, data):
        u = self.db.session.query(User).get(user['id'])
        modified = False

        for k, v in data.items():
            if k == 'name':
                u.name = v
                modified = True
            elif k == 'username':
                u.username = v
                modified = True
            elif k == 'email':
                u.email = v
                modified = True
            elif k == 'password':
                u.password = v
                modified = True

        self.db.session.commit()

        user_id = u.id
        return self.get_user(user_id), modified

    def remove_user(self, user):
        u = self.db.session.query(User).get(user['id'])
        self.db.session.delete(u)

        self.db.session.commit()

    def get_projects(self, user_id):
        res = self.db.session.query(Project).join(User).filter(User.id == user_id)

        res_list = []
        for project in res:
            res_list.append(as_dict(project))

        self.db.session.close()
        return res_list

    def get_project(self, pk, user_id):
        res = self.db.session.query(Project).join(User).filter(User.id == user_id).filter(Project.id == pk).first()

        project = as_dict(res)
        return project

    def get_project_load(self, pk, user_id):
        res = self.db.session.query(Project).join(User).filter(User.id == user_id).filter(Project.id == pk).first()

        return res

    def add_project(self, project, user_id):
        project_obj = Project(project['title'], user_id)

        self.db.session.add(project_obj)
        self.db.session.commit()

        dic = as_dict(project_obj)

        return dic

    def update_project(self, project, user_id, data):
        p = self.db.session.query(Project).get(project['id'])

        for k, v in data.items():
            if k == 'title':
                p.title = v
        p.last_updated = datetime.now()

        self.db.session.commit()

        project_id = p.id
        return self.get_project(project_id, user_id)

    def remove_project(self, project):
        p = self.db.session.query(Project).get(project['id'])
        self.db.session.delete(p)

        self.db.session.commit()

    def get_tasks(self, project_pk):
        res = self.db.session.query(Task).join(Project).filter(Project.id == project_pk)
        res_list = []
        for task in res:
            res_list.append(as_dict(task))

        return res_list

    def get_task(self, project_pk, pk):
        res = self.db.session.query(Task).join(Project).filter(Project.id == project_pk).filter(Task.id == pk)
        final_task = None
        for task in res:
            final_task = (as_dict(task))

        return final_task

    def add_task(self, task, project_pk):
        order = self.db.session.query(Task).join(Project).filter(Project.id == project_pk).count() + 1
        if 'due_date' in task:
            date = datetime.strptime(task['due_date'], "%a, %d %b %Y %H:%M:%S %Z")
        else:
            date = datetime.now() + timedelta(days=2)
        task_obj = Task(task['title'], order, date, False, project_pk)

        self.db.session.add(task_obj)
        self.db.session.commit()

        dic = as_dict(task_obj)

        return dic

    def update_task(self, project_pk, task, data):
        t = self.db.session.query(Task).get(task['id'])

        for k, v in data.items():
            if k == 'title':
                t.title = v
            if k == 'due_date':
                t.date = datetime.strptime(v, "%a, %d %B %Y %H:%M:%S %Z")
            if k == 'completed':
                t.completed = v

        self.db.session.commit()

        task_id = t.id
        return self.get_task(project_pk, task_id)

    def remove_task(self, task):
        t = self.db.session.query(Task).get(task['id'])
        self.db.session.delete(t)

        self.db.session.commit()
