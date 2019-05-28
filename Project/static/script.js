/**
 * REST Client
 *
 */

function getUsers() {
    var req = new XMLHttpRequest();
    req.open("GET", "/api/users/");
    req.addEventListener("load", function() {
        var users = JSON.parse(this.responseText);
        var ul = document.getElementById('users');
        ul.innerHTML = '';
        for (var i in users) {
            var li = document.createElement('li');
            li.innerHTML = users[i].name + ' (' + users[i].username + ') -' + users[i].email;
            li.innerHTML += " <button onclick='updateUser(" + users[i].id + ")'>Update</button>";
            li.innerHTML += " <button onclick='deleteUser(" + users[i].id + ")'>Delete</button>";
            ul.appendChild(li);
        }
    });
    req.send();
}

function addUser() {
    var form = document.getElementById("form");
    var name = form.name.value;
    var username = form.username.value;
    var email = form.email.value;
    var password = form.password.value;

    var req = new XMLHttpRequest();
    req.open("POST", "/api/users/");
    let json = JSON.stringify({
        name: name,
        username: username,
        email: email,
        password: password
    });
    req.addEventListener("load", function() {
        getUsers();
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);
}

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

    req.addEventListener("load", function() {
        getUsers();
    });
    req.setRequestHeader("Content-type", "application/json");
    req.send(json);

}

function deleteUser(id) {
    var req = new XMLHttpRequest();
    req.open("DELETE", "/api/users/" + id + "/");
    req.addEventListener("load", function() {
        getUsers();
    });
    req.send();
}

function getProjects() {
    var req = new XMLHttpRequest();
    req.open("GET", "/api/projects/");
    req.addEventListener("load", function() {
        var projects = JSON.parse(this.responseText);
        var ul = document.getElementById('projects');
        ul.innerHTML = '';
        for (var i in projects) {
            var li = document.createElement('li');
            li.innerHTML = projects[i].title + ' (' + projects[i].user + ') -' + projects[i].creation_date + ' to end at: ' + projects[i].last_updated;
            ul.appendChild(li);
        }
    });
    req.send();
}

getUsers();
getProjects();
