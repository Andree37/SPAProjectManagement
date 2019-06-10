/**
 * REST Client
 *
 */

function signupUser() {
    var form = document.getElementById("signup_form");

    var username = form.uname.value;
    var password = form.psw.value;
    var email = form.email.value;
    var name = form.name.value;

    var req = new XMLHttpRequest();
    req.open("POST", "/api/user/register/");
    let json = JSON.stringify({
        name: name,
        username: username,
        email: email,
        password: password
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);
    location.reload();
}

function loginUser() {
    var form = document.getElementById("login_form");
    var username = form.uname.value;
    var password = form.psw.value;

    var req = new XMLHttpRequest();
    req.open("POST", "/api/user/login/");
    let json = JSON.stringify({
        username: username,
        password: password
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);

    req.onload = function () {
        if (req.status === 200) {
            getUser();
            getProjects();
            location.reload();
        }
    }
}

function getUser() {
    var req = new XMLHttpRequest();
    req.open("GET", "/api/user/");
    req.addEventListener("load", function () {
        var user = JSON.parse(this.responseText);
        if (user !== "") {
            document.getElementById("div_login").innerHTML = "<ul class='nav navbar-nav navbar-right'><li><a href='#'><span class='glyphicon glyphicon-user'></span>" + user.username +
                "</a></li> <li onclick='logout();'><a href='#'><span class='glyphicon glyphicon-log-in'></span> Logout</a></li></ul>";
        }
        else {
            document.getElementById("div_login").innerHTML = " <ul class='nav navbar-nav navbar-right'><li onclick='document.getElementById('signup').style.display='block''><a href='#'><span class='glyphicon glyphicon-user'></span> Sign Up</a></li><li onclick='document.getElementById('login').style.display='block''><a href='#'><spanclass='glyphicon glyphicon-log-in'></span> Login</a></li></ul>"
        }
    });
    req.send();
}

function logout() {
    var req = new XMLHttpRequest();
    req.open("GET", "/api/user/logout/");
    req.send();
    req.addEventListener("load", function () {
        location.reload();
    });
}

// check this
function updateUser(id) {
    var form = document.getElementById("form");
    var name = form.name.value;
    var username = form.username.value;
    var email = form.email.value;
    var password = form.password.value;


    var req = new XMLHttpRequest();
    req.open("PUT", "/api/users/" + id + "/");
    let json;
    json = JSON.stringify({
        name: name,
        username: username,
        email: email,
        password: password
    });

    req.addEventListener("load", function () {
        getUsers();
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);

}

//check this
function deleteUser(id) {
    var req = new XMLHttpRequest();
    req.open("DELETE", "/api/users/" + id + "/");
    req.addEventListener("load", function () {
        getUsers();
    });
    req.send();
}

function getProjects() {
    var req = new XMLHttpRequest();
    req.open("GET", "/api/projects/");
    req.addEventListener("load", function () {
        var projects = JSON.parse(this.responseText);
        var table = document.getElementById('projects_table');
        table.innerHTML = "";
        for (var i in projects) {
            let div = document.createElement("div");
            div.setAttribute("id", "project" + projects[i].id);
            div.setAttribute("class", "w3-panel w3-card");
            div.setAttribute("style", "padding-top: 2vh; margin-right: 4vh; width: 25%; display: inline-block;");
            div.textContent = projects[i].title + projects[i].creation_date + " to end at: " + projects[i].last_updated;

            table.appendChild(div);
            getTasks(projects[i].id);
        }
    });
    req.send();

}

function getTasks(project_id) {
    var req_tasks = new XMLHttpRequest();
    task_api = "/api/projects/" + project_id + "/tasks/";
    req_tasks.open("GET", task_api);
    req_tasks.addEventListener("load", function () {
        var tasks = JSON.parse(this.responseText);
        var project = document.getElementById("project" + project_id);
        var div = document.createElement("div");
        var ul = document.createElement("ul");
        ul.setAttribute("id", "list"+project_id);
        ul.setAttribute("style", "padding: 0; margin: 0; margin-top: 1vh; list-style: none;");

        div.setAttribute("style", "display: inline");
        for (var j in tasks) {
            let content = document.createElement("p");
            content.setAttribute("style", "display: inline; width: 90% margin: 0; text-decoration: none");
            content.textContent = "| " + tasks[j].title;

            let checkbox_div = document.createElement("div");
            let checkbox = document.createElement("input");
            checkbox.setAttribute("type", "checkbox");
            if (tasks[j].completed === true) {
                checkbox.setAttribute("checked", "true");
                content.setAttribute("style", "display: inline; width: 90% margin: 0; text-decoration: line-through;");
            }
            checkbox.setAttribute("onClick", "setTaskState(" + project_id + ", " + tasks[j].id + ", " + tasks[j].completed + ")");
            checkbox_div.setAttribute("style", "display: inline; margin-right: 1vh;");
            checkbox_div.appendChild(checkbox);

            let li = document.createElement("li");
            li.setAttribute("id", "task" + tasks[j].id);
            li.setAttribute("draggable", "true");
            li.setAttribute("ondragstart", "drag(event, list" +project_id+")");
            li.setAttribute("ondrop", "ev.dataTransfer.dropEffect = 'none'");
            li.setAttribute("style", "padding: 0; margin: 0; width: 70%; display: inline;");

            let remove = document.createElement("a");
            let remove_span = document.createElement("span");
            remove_span.setAttribute("class", "glyphicon glyphicon-remove-sign");
            remove.setAttribute("onClick", "removeTask(" + project_id + ", " + tasks[j].id + ") ");
            remove.setAttribute("style", "display: inline; margin-left: 1vh;");
            remove.appendChild(remove_span);

            let line = document.createElement("p");
            line.appendChild(checkbox_div);
            line.appendChild(content);
            line.appendChild(remove);

            li.appendChild(line);
            ul.appendChild(li);
        }
        div.appendChild(ul);

        bottom_div = document.createElement("div");

        let textField = document.createElement("input");
        textField.setAttribute("type", "text");
        textField.setAttribute("style", "width: 60%; padding: 0.5vh;");
        textField.setAttribute("id", "txt" + project_id);

        let button = document.createElement("button");
        button.setAttribute("class", "btn btn-outline-info");
        button.setAttribute("style", "margin-bottom: 1vh ;margin-left: 5%; width: 35%;");
        button.setAttribute("onClick", "addTask(" + project_id + ")");
        button.textContent = "Add Task";

        bottom_div.appendChild(textField);
        bottom_div.appendChild(button);
        div.appendChild(bottom_div);

        project.appendChild(div);
    });
    req_tasks.send();
}

function setTaskState(project_id, task_id, state) {
    var req = new XMLHttpRequest();
    req.open("PUT", "/api/projects/" + project_id + "/tasks/" + task_id + "/");
    req.addEventListener("load", function () {
        getProjects();
    });
    new_state = !state;
    let json = JSON.stringify({
        completed: new_state
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);
}

function removeTask(project_id, task_id) {
    var task = document.getElementById("task" + task_id);
    task.parentNode.removeChild(task);
    var req = new XMLHttpRequest();
    req.open("DELETE", "/api/projects/" + project_id + "/tasks/" + task_id + "/");
    req.addEventListener("load", function () {
        getProjects();
    });
    req.send();
}

function addTask(project_id) {
    var textField = document.getElementById("txt" + project_id);
    var title = textField.value;
    var req = new XMLHttpRequest();
    req.open("POST", "/api/projects/" + project_id + "/tasks/");
    req.addEventListener("load", function () {
        textField.textContent = "";
        getProjects();
    });
    let json = JSON.stringify({
        title: title
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);
}


getUser();
getProjects();