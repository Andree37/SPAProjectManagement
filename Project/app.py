"""
 Flask REST application

"""
from flask import Flask, request, jsonify, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from db import DataBase, User, Project, Task
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = "\xe7utGZI\xf6'\x95\xbe\xd1\x84\xac\xbb\xf1n"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_USERNAME'] = 'scp405testsubject@gmail.com'
app.config['MAIL_PASSWORD'] = 'thesenderone201'
app.config['MAIL_DEFAULT_SENDER'] = 'scp405testsubject@gmail.com'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = app.debug
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = app.testing
app.config['MAIL_ASCII_ATTACHMENTS'] = False


db = DataBase(app)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.username == "dani"


# admin for all the tables
admin = Admin(app)
admin.add_view(MyModelView(User, db.db.session))
admin.add_view(MyModelView(Project, db.db.session))
admin.add_view(MyModelView(Task, db.db.session))


@app.route('/')
def index():
    return app.send_static_file('index.html')


@login_manager.user_loader
def load_user(user_id):
    return db.get_user_load(user_id)


@app.route('/api/user/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = ""
    password = ""
    authenticated = False
    if data is not None:
        if 'username' in data:
            username = data['username']
        if 'password' in data:
            password = data['password']

    if data is None or username == "" or password == "":
        # change the 404
        return make_response(jsonify(), 404)

    user = db.get_user_login(username, password)
    if user is None:
        return make_response(jsonify(), 404)

    authenticated = user.authenticated

    # Check for validation of the sent email
    if not authenticated:
        return make_response(jsonify(), 401)

    # if user exists and the fields are verified, login
    login_user(user, remember=True)

    return make_response(jsonify(), 200)


@app.route('/api/authenticate/<string:key>/', methods=['GET'])
def authenticate(key):
    user = db.get_user_from_authkey(key)
    if user is None:
        return make_response(jsonify(), 401)

    authenticated = db.authenticate_user(user.id)
    if authenticated:
        return make_response(jsonify(), 200)

    return make_response(jsonify(), 404)


@app.route('/api/user/register/', methods=['POST'])
def register():
    user_json = request.get_json()
    user = db.add_user(user_json)
    if user is None:
        return make_response(jsonify(), 409)

    # Send user the email with the verification
    # For testing purposes, the emails are always sent to this throwaway account
    msg = Message("Authenticate here",
                  recipients=["scp404testsubject@gmail.com"])
    msg.body = f"http://localhost:8000/api/authenticate/{user['auth_key']}/"
    mail.send(msg)

    return make_response(jsonify(user), 201)


@app.route('/api/user/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return make_response(jsonify(), 200)


# check good
@app.route("/api/user/", methods=['GET', 'DELETE', 'PUT'])
@login_required
def single_user():
    user = db.get_user(current_user.id)
    if user is None:
        return make_response(jsonify(), 404)

    if request.method == 'GET':
        return make_response(jsonify(user), 200)
    elif request.method == 'DELETE':
        db.remove_user(user)
        return make_response(jsonify(), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        updated_user, modified = db.update_user(user, data)
        if not modified:
            return make_response(jsonify(), 404)
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
        project = db.add_project(project_json, user.id)

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
        updated_project = db.update_project(project, user.id, data)
        return make_response(jsonify(updated_project), 200)


# check done
# check if user has project
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
