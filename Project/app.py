"""
 Flask REST application

"""
import datetime

from flask import Flask, request, jsonify, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from db import DataBase

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = "\xe7utGZI\xf6'\x95\xbe\xd1\x84\xac\xbb\xf1n"

db = DataBase(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@login_manager.user_loader
def load_user(user_id):
    return db.get_user_load(user_id)


@app.route('/api/user/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = db.get_user_login(username, password)
    login_user(user, remember=True)

    return make_response("You are now logged in", 200)


@app.route('/api/user/register/', methods=['POST'])
def register():
    user_json = request.get_json()
    user = db.add_user(user_json)

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
        users = db.get_users()

        return make_response(jsonify(users), 200)

    elif request.method == 'POST':
        user_json = request.get_json()
        user = db.add_user(user_json)

        return make_response(jsonify(user), 201)


# check good
@app.route("/api/user/<int:pk>/", methods=['GET', 'DELETE', 'PUT'])
def single_user(pk):
    user = db.get_user(pk)
    if user is None:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(user), 200)
    elif request.method == 'DELETE':
        db.remove_user(user)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_user = db.update_user(user, data)
        return make_response(jsonify(updated_user), 200)


# check good
@app.route("/api/projects/", methods=['GET', 'POST'])
@login_required
def all_projects():
    user = current_user
    if request.method == 'GET':
        projects = db.get_projects(user.id)
        if projects is None:
            return make_response(jsonify(), 404)
        return make_response(jsonify(projects), 200)

    elif request.method == 'POST':
        project_json = request.get_json()
        project = db.add_project(project_json)

        return make_response(jsonify(project), 201)


# check good
@app.route("/api/projects/<int:pk>/", methods=['GET', 'DELETE', 'PUT'])
@login_required
def single_project(pk):
    user = current_user
    project = db.get_project(pk, user.id)
    if len(project) == 0:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(project), 200)
    elif request.method == 'DELETE':
        db.remove_project(project)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_project = db.update_project(project, data)
        return make_response(jsonify(updated_project), 200)


# check done
@app.route("/api/projects/<int:project_pk>/tasks/", methods=['GET', 'POST'])
@login_required
def all_tasks(project_pk):
    user = current_user
    project = db.get_project_load(project_pk, user.id)
    if request.method == 'GET':
        tasks = db.get_tasks(project.id)
        if len(tasks) == 0:
            return make_response(jsonify(), 404)
        return make_response(jsonify(tasks), 200)

    elif request.method == 'POST':
        task_json = request.get_json()
        task = db.add_task(task_json, project_pk)

        return make_response(jsonify(task), 201)


# check done
@app.route("/api/projects/<int:project_pk>/tasks/<int:pk>/", methods=['GET', 'DELETE', 'PUT'])
@login_required
def single_task(project_pk, pk):
    user = current_user
    project = db.get_project_load(project_pk, user.id)
    task = db.get_task(project.id, pk)
    if task is None:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(task), 200)
    elif request.method == 'DELETE':
        db.remove_task(task)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_task = db.update_task(project_pk, task, data)
        return make_response(jsonify(updated_task), 200)


# to run the app
app.run(host='0.0.0.0', port=8000, debug=True)
