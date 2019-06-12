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
    req.addEventListener("load", function () {
        login(username, password);
    });
}

function login(username, password) {
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
        if (req.status == 401) {
            return;
        }
        var user = JSON.parse(this.responseText);
        if (user !== "") {
            document.getElementById("div_login").innerHTML = "<ul class='nav navbar-nav navbar-right'><li onClick= document.getElementById('uprofile').style.display='block'><a href='#'><span class='glyphicon glyphicon-user'></span>" + user.username +
                "</a></li> <li onclick='logout('true');'><a href='#'><span class='glyphicon glyphicon-log-in'></span> Logout</a></li></ul>";
            document.getElementById("btn_addProject").setAttribute("style", "margin-left: 80%; margin-right:5%; width: 15%");
            var profile = document.getElementById("profile_form");
            profile.name.setAttribute("placeholder", user.name);
            profile.name.value = "";
            profile.uname.setAttribute("placeholder", user.username);
            profile.uname.value = "";
            profile.email.setAttribute("placeholder", user.email);
            profile.email.value = "";
        }
        else {
            document.getElementById("div_login").innerHTML = " <ul class='nav navbar-nav navbar-right'><li onclick='document.getElementById('signup').style.display='block''><a href='#'><span class='glyphicon glyphicon-user'></span> Sign Up</a></li><li onclick='document.getElementById('login').style.display='block''><a href='#'><spanclass='glyphicon glyphicon-log-in'></span> Login</a></li></ul>"
        }
    });
    req.send();
}

function logout(reload) {
    var req = new XMLHttpRequest();
    req.open("GET", "/api/user/logout/");
    req.send();
    req.addEventListener("load", function () {
        if (reload == true) {
            location.reload();
        }
    });
}

function updateUser() {
    var form = document.getElementById("profile_form");
    var name = form.name.value;
    var username = form.uname.value;
    var email = form.email.value;
    console.log(username);
    var req = new XMLHttpRequest();
    req.open("PUT", "/api/user/");
    let json = JSON.stringify({
        name: name,
        username: username,
        email: email,
    });

    req.addEventListener("load", function () {
        location.reload();
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);

}

function deleteUser() {
    var req = new XMLHttpRequest();
    logout(false);
    req.open("DELETE", "/api/user/");
    req.addEventListener("load", function () {
        location.reload();
    });
    req.send();
}

function getProjects() {
    var req = new XMLHttpRequest();
    req.open("GET", "/api/projects/");
    req.addEventListener("load", function () {
        if (req.status != 200) {
            return;
        }
        var projects = JSON.parse(this.responseText);
        var table = document.getElementById('projects_table');
        table.innerHTML = "";
        for (var i in projects) {
            let div = document.createElement("div");
            div.setAttribute("id", "project" + projects[i].id);
            div.setAttribute("class", "w3-panel w3-card");
            div.setAttribute("style", "padding-top: 2vh; margin-right: 4vh; width: 25%; display: inline-block;");
            div.textContent = projects[i].title + projects[i].creation_date + " to end at: " + projects[i].last_updated;

            let button = document.createElement("button");
            button.setAttribute("type", "button");
            button.setAttribute("class", "btn btn-outline-danger");
            button.setAttribute("onClick", "removeProject(" + projects[i].id + ")")
            button.textContent = "Remove Project";

            let button_div = document.createElement("div");
            button_div.appendChild(button);

            div.appendChild(button_div);
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
        ul.setAttribute("id", "list" + project_id);
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
            li.setAttribute("ondragstart", "drag(event, list" + project_id + ")");
            li.setAttribute("ondrop", "ev.dataTransfer.dropEffect = 'none'");
            li.setAttribute("style", "padding: 0; margin: 0; width: 70%; display: inline;");

            let remove = document.createElement("a");
            let remove_span = document.createElement("span");
            remove_span.setAttribute("class", "glyphicon glyphicon-remove-sign");
            remove.setAttribute("onClick", "removeTask(" + project_id + ", " + tasks[j].id + ") ");
            remove.setAttribute("style", "display: inline; margin-left: 1vh;");
            remove.appendChild(remove_span);

            let line = document.createElement("p");
            line.setAttribute("id", "line" + tasks[j].id);
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
        if (req.status != 200) {
            return;
        }
        var task = JSON.parse(this.responseText);
        let li = document.getElementById("task" + task_id);

        let old_p = document.getElementById("line" + task_id);
        old_p.parentNode.removeChild(old_p);

        let content = document.createElement("p");
        content.setAttribute("style", "display: inline; width: 90% margin: 0; text-decoration: none");
        content.textContent = "| " + task.title;

        let checkbox_div = document.createElement("div");
        let checkbox = document.createElement("input");
        checkbox.setAttribute("type", "checkbox");
        if (task.completed === true) {
            checkbox.setAttribute("checked", "true");
            content.setAttribute("style", "display: inline; width: 90% margin: 0; text-decoration: line-through;");
        }
        checkbox.setAttribute("onClick", "setTaskState(" + project_id + ", " + task.id + ", " + task.completed + ")");
        checkbox_div.setAttribute("style", "display: inline; margin-right: 1vh;");
        checkbox_div.appendChild(checkbox);

        li.setAttribute("id", "task" + task.id);
        li.setAttribute("draggable", "true");
        li.setAttribute("ondragstart", "drag(event, list" + project_id + ")");
        li.setAttribute("ondrop", "ev.dataTransfer.dropEffect = 'none'");
        li.setAttribute("style", "padding: 0; margin: 0; width: 70%; display: inline;");

        let remove = document.createElement("a");
        let remove_span = document.createElement("span");
        remove_span.setAttribute("class", "glyphicon glyphicon-remove-sign");
        remove.setAttribute("onClick", "removeTask(" + project_id + ", " + task.id + ") ");
        remove.setAttribute("style", "display: inline; margin-left: 1vh;");
        remove.appendChild(remove_span);

        let line = document.createElement("p");
        line.setAttribute("id", "line" + task.id);
        line.appendChild(checkbox_div);
        line.appendChild(content);
        line.appendChild(remove);

        li.appendChild(line);

    });
    new_state = !state;
    let json = JSON.stringify({
        completed: new_state
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);
}

function removeTask(project_id, task_id) {
    var req = new XMLHttpRequest();
    req.open("DELETE", "/api/projects/" + project_id + "/tasks/" + task_id + "/");
    req.addEventListener("load", function () {
        if (req.status != 200) {
            return;
        }
        let li = document.getElementById("task" + task_id)
        li.parentNode.removeChild(li);
    });
    req.send();
}

function addTask(project_id) {
    var textField = document.getElementById("txt" + project_id);
    var title = textField.value;
    var req = new XMLHttpRequest();
    req.open("POST", "/api/projects/" + project_id + "/tasks/");
    req.addEventListener("load", function () {
        if (req.status != 201) {
            return;
        }

        textField.value = "";

        var task = JSON.parse(this.responseText);
        let div = document.getElementById("project" + project_id);
        let ul = div.childNodes[2].childNodes[0];

        let content = document.createElement("p");
        content.setAttribute("style", "display: inline; width: 90% margin: 0; text-decoration: none");
        content.textContent = "| " + task.title;

        let checkbox_div = document.createElement("div");
        let checkbox = document.createElement("input");
        checkbox.setAttribute("type", "checkbox");
        if (task.completed === true) {
            checkbox.setAttribute("checked", "true");
            content.setAttribute("style", "display: inline; width: 90% margin: 0; text-decoration: line-through;");
        }
        checkbox.setAttribute("onClick", "setTaskState(" + project_id + ", " + task.id + ", " + task.completed + ")");
        checkbox_div.setAttribute("style", "display: inline; margin-right: 1vh;");
        checkbox_div.appendChild(checkbox);

        let li = document.createElement("li");
        li.setAttribute("id", "task" + task.id);
        li.setAttribute("draggable", "true");
        li.setAttribute("ondragstart", "drag(event, list" + project_id + ")");
        li.setAttribute("ondrop", "ev.dataTransfer.dropEffect = 'none'");
        li.setAttribute("style", "padding: 0; margin: 0; width: 70%; display: inline;");

        let remove = document.createElement("a");
        let remove_span = document.createElement("span");
        remove_span.setAttribute("class", "glyphicon glyphicon-remove-sign");
        remove.setAttribute("onClick", "removeTask(" + project_id + ", " + task.id + ") ");
        remove.setAttribute("style", "display: inline; margin-left: 1vh;");
        remove.appendChild(remove_span);

        let line = document.createElement("p");
        line.setAttribute("id", "line" + task.id);
        line.appendChild(checkbox_div);
        line.appendChild(content);
        line.appendChild(remove);

        li.appendChild(line);
        ul.appendChild(li);

    });
    let json = JSON.stringify({
        title: title
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);
}

// todo
function updateTask() {

}

function addProject() {
    var form = document.getElementById("project_form");
    var title = form.title.value;

    var req = new XMLHttpRequest();
    req.open("POST", "/api/projects/");
    let json = JSON.stringify({
        title: title,
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);

    req.onload = function () {
        if (req.status === 201) {
            var project = JSON.parse(this.responseText);
            var table = document.getElementById('projects_table');
            let div = document.createElement("div");
            div.setAttribute("id", "project" + project.id);
            div.setAttribute("class", "w3-panel w3-card");
            div.setAttribute("style", "padding-top: 2vh; margin-right: 4vh; width: 25%; display: inline-block;");
            div.textContent = project.title + project.creation_date + " to end at: " + project.last_updated;

            let button = document.createElement("button");
            button.setAttribute("type", "button");
            button.setAttribute("class", "btn btn-outline-danger");
            button.setAttribute("onClick", "removeProject(" + project.id + ")")
            button.textContent = "Remove Project";

            let button_div = document.createElement("div");
            button_div.appendChild(button);

            div.appendChild(button_div);

            table.appendChild(div);
            getTasks(project.id);
            document.getElementById('project_add').style.display = 'none'
        }
    }
}

function removeProject(project_id) {
    var req = new XMLHttpRequest();
    req.open("DELETE", "/api/projects/" + project_id + "/");
    req.addEventListener("load", function () {
        if (req.status != 200) {
            return;
        }
        let div = document.getElementById("project" + project_id)
        div.parentNode.removeChild(div);
    });
    req.send();
}

// todo
function updateProject() {
    
}

getUser();
getProjects();