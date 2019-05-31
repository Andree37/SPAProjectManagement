"""
 Flask REST application

"""
import datetime

from flask import Flask, request, jsonify, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from datetime import datetime, timedelta
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

global app
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = "\xe7utGZI\xf6'\x95\xbe\xd1\x84\xac\xbb\xf1n"

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@login_manager.user_loader
def load_user(user_id):
    return get_user_load(user_id)


@app.route('/api/user/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = get_user_login(username, password)
    login_user(user)

    return make_response("You are now logged in", 200)


@app.route('/api/user/register/', methods=['POST'])
def register():
    user_json = request.get_json()
    user = add_user(user_json)

    return make_response(jsonify(user), 201)


@app.route('/api/user/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return make_response("You are now logged out", 200)


# check good
@app.route("/api/user/", methods=['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        users = get_users()

        return make_response(jsonify(users),200)

    elif request.method == 'POST':
        user_json = request.get_json()
        user = add_user(user_json)

        return make_response(jsonify(user), 201)


# check good
@app.route("/api/user/<int:pk>/", methods=['GET', 'DELETE', 'PUT'])
def single_user(pk):
    user = get_user(pk)
    if user is None:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(user), 200)
    elif request.method == 'DELETE':
        remove_user(user)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_user = update_user(user, data)
        return make_response(jsonify(updated_user), 200)


# check good
@app.route("/api/projects/", methods=['GET', 'POST'])
@login_required
def all_projects():
    user = current_user
    if request.method == 'GET':
        projects = get_projects(user.id)
        if projects is None:
            return make_response(jsonify(), 404)
        return make_response(jsonify(projects), 200)

    elif request.method == 'POST':
        project_json = request.get_json()
        project = add_project(project_json)

        return make_response(jsonify(project), 201)


# check good
@app.route("/api/projects/<int:pk>/", methods=['GET', 'DELETE', 'PUT'])
@login_required
def single_project(pk):
    user = current_user
    project = get_project(pk, user.id)
    if len(project) == 0:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(project), 200)
    elif request.method == 'DELETE':
        remove_project(project)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_project = update_project(project, data)
        return make_response(jsonify(updated_project), 200)


# check done
@app.route("/api/projects/<int:project_pk>/tasks/", methods=['GET', 'POST'])
@login_required
def all_tasks(project_pk):
    user = current_user
    project = get_project_load(project_pk, user.id)
    if request.method == 'GET':
        tasks = get_tasks(project.id)
        if len(tasks) == 0:
            return make_response(jsonify(), 404)
        return make_response(jsonify(tasks), 200)

    elif request.method == 'POST':
        task_json = request.get_json()
        task = add_task(task_json, project_pk)

        return make_response(jsonify(task), 201)


# check done
@app.route("/api/projects/<int:project_pk>/tasks/<int:pk>/", methods=['GET', 'DELETE', 'PUT'])
@login_required
def single_task(project_pk, pk):
    user = current_user
    project = get_project_load(project_pk, user.id)
    task = get_task(project.id, pk)
    if task is None:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(task), 200)
    elif request.method == 'DELETE':
        remove_task(task)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_task = update_task(project_pk, task, data)
        return make_response(jsonify(updated_task), 200)


# Database related

db = SQLAlchemy(app)


# Tables for the db
class User(db.Model, UserMixin):
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


class Project(db.Model):
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


class Task(db.Model):
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


# admin for all the tables
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Task, db.session))


def as_dict(obj):
    if obj is None:
        return {}
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def recreate_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    ana = User('Ana', "anocas", "anocas@gmail.com", "123")
    paulo = User('Paulo', "paulocas", "paulinho@yahoo.com", "123")

    project1 = Project("first project", 1)
    project2 = Project("second project", 2)
    due_date = datetime.now() + timedelta(days=2)
    task1 = Task("task1", 1, due_date, False, 1)
    task2 = Task("task2", 1, due_date, False, 2)

    db.session.add(ana)
    db.session.add(paulo)
    db.session.add(project1)
    db.session.add(project2)
    db.session.add(task1)
    db.session.add(task2)

    db.session.commit()


def get_users():
    res = db.session.query(User).all()
    res_list = []
    for user in res:
        res_list.append(as_dict(user))

    return res_list


def get_user(pk):
    res = db.session.query(User).get(pk)

    user = as_dict(res)
    return user


def get_user_load(pk):
    res = db.session.query(User).get(pk)

    return res


def get_user_login(username, password):
    res = db.session.query(User).filter_by(username=username, password=password).first()
    return res


def add_user(user):
    user_obj = User(user['name'], user['username'], user['email'], user['password'])

    db.session.add(user_obj)
    db.session.commit()

    dic = as_dict(user_obj)

    return dic


def update_user(user, data):
    u = db.session.query(User).get(user['id'])

    for k, v in data.items():
        if k == 'name':
            u.name = v
        if k == 'username':
            u.username = v
        if k == 'email':
            u.email = v
        if k == 'password':
            u.password = v

    db.session.commit()

    user_id = u.id
    return get_user(user_id)


def remove_user(user):
    u = db.session.query(User).get(user['id'])
    db.session.delete(u)

    db.session.commit()


def get_projects(user_id):
    res = db.session.query(Project).join(User).filter(User.id == user_id)

    res_list = []
    for project in res:
        res_list.append(as_dict(project))

    db.session.close()
    return res_list


def get_project(pk, user_id):
    res = db.session.query(Project).join(User).filter(User.id == user_id).filter(Project.id == pk).first()

    project = as_dict(res)
    return project


def get_project_load(pk, user_id):
    res = db.session.query(Project).join(User).filter(User.id == user_id).filter(Project.id == pk).first()

    return res


def add_project(project):
    project_obj = Project(project['title'], project['user'])

    db.session.add(project_obj)
    db.session.commit()

    dic = as_dict(project_obj)

    return dic


def update_project(project, data):
    p = db.session.query(Project).get(project['id'])

    for k, v in data.items():
        if k == 'title':
            p.title = v
    p.last_updated = datetime.now()

    db.session.commit()

    project_id = p.id
    return get_project(project_id)


def remove_project(project):
    p = db.session.query(Project).get(project['id'])
    db.session.delete(p)

    db.session.commit()


def get_tasks(project_pk):
    res = db.session.query(Task).join(Project).filter(Project.id == project_pk)
    res_list = []
    for task in res:
        res_list.append(as_dict(task))

    return res_list


def get_task(project_pk, pk):
    res = db.session.query(Task).join(Project).filter(Project.id == project_pk).filter(Task.id == pk)
    final_task = None
    for task in res:
        final_task = (as_dict(task))

    return final_task


def add_task(task, project_pk):
    order = db.session.query(Task).join(Project).filter(Project.id == project_pk).count() + 1
    date = datetime.strptime(task['due_date'], "%a, %d %B %Y %H:%M:%S %Z")
    task_obj = Task(task['title'], order, date, task['completed'],
                    task['project'])

    db.session.add(task_obj)
    db.session.commit()

    dic = as_dict(task_obj)

    return dic


def update_task(project_pk, task, data):
    t = db.session.query(Task).get(task['id'])

    for k, v in data.items():
        if k == 'title':
            t.title = v
        if k == 'due_date':
            t.date = datetime.strptime(v, "%a, %d %B %Y %H:%M:%S %Z")
        if k == 'completed':
            t.completed = v

    db.session.commit()

    task_id = t.id
    return get_task(project_pk, task_id)


def remove_task(task):
    t = db.session.query(Task).get(task['id'])
    db.session.delete(t)

    db.session.commit()


# to run the app
# recreate_db()
app.run(host='0.0.0.0', port=8000, debug=True)
