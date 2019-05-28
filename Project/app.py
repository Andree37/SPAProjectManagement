"""
 Flask REST application

"""

from flask import Flask, request, jsonify, make_response
import db

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route("/api/users/", methods=['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        users = db.get_users()

        return make_response(jsonify(users))

    elif request.method == 'POST':
        user_json = request.get_json()
        user = db.add_user(user_json)

        return make_response(jsonify(user), 201)


@app.route("/api/users/<int:pk>/", methods=['GET', 'DELETE', 'PUT'])
def single_user(pk):
    user = db.get_user(pk)
    if user is None:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(user))
    elif request.method == 'DELETE':
        db.remove_user(user)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_user = db.update_user(user, data)
        return make_response(jsonify(updated_user), 200)


@app.route("/api/projects/", methods=['GET', 'POST'])
def all_projects():
    if request.method == 'GET':
        projects = db.get_projects()

        return make_response(jsonify(projects))

    elif request.method == 'POST':
        project_json = request.get_json()
        project = db.add_project(project_json)

        return make_response(jsonify(project), 201)


@app.route("/api/projects/<int:pk>/", methods=['GET', 'DELETE', 'PUT'])
def single_project(pk):
    project = db.get_project(pk)
    if project is None:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(project))
    elif request.method == 'DELETE':
        db.remove_project(project)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_project = db.update_project(project, data)
        return make_response(jsonify(updated_project), 200)


@app.route("/api/projects/<int:pk>/tasks/", methods=['GET', 'POST'])
def all_tasks():
    if request.method == 'GET':
        tasks = db.get_tasks()

        return make_response(jsonify(tasks))

    elif request.method == 'POST':
        task_json = request.get_json()
        task = db.add_project(task_json)

        return make_response(jsonify(task), 201)


@app.route("/api/projects/<int:pk>/tasks/<int:pk>", methods=['GET', 'DELETE', 'PUT'])
def single_task(pk):
    task = db.get_task(pk)
    if task is None:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(task))
    elif request.method == 'DELETE':
        db.remove_task(task)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_task = db.update_task(task, data)
        return make_response(jsonify(updated_task), 200)


db.recreate_db()
app.run(host='0.0.0.0', port=8000, debug=True)
