function login(token){

    token = JSON.parse(token);
    sessionStorage.setItem("token", token.token);

    var request = new XMLHttpRequest();
    request.open('GET', 'http://127.0.0.1:8000/user/');
    request.setRequestHeader("Authorization", "Bearer " + token.token);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Accept', 'application/json');

    request.onload = function() {
        const status = request.status;

        if (status === 202) {
            window.location.replace("welcome.html");
        }
    }

    request.send();
    
}

function getToken(){

    let Email = document.getElementById("Email");
    let Password = document.getElementById("Password");


    var request = new XMLHttpRequest();
    request.open('GET', 'http://127.0.0.1:8000/user/validate/');
    request.setRequestHeader("Authorization", "Basic " + btoa(Email.value + ":" + Password.value));
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Accept', 'application/json');

    request.onload = function() {
        const status = request.status;

        if (status === 202) {
           login(request.responseText);
        }
    }

    request.send();   
}

function singup(){
    let Email = document.getElementById("Email");
    let Password = document.getElementById("Password");
    let PasswordC = document.getElementById("PasswordC");

    console.log(Email.value);
    console.log(Password.value);
    console.log(PasswordC.value);

    if (Password.value !== PasswordC.value){
        window.alert("Passwords don't match");        
    }
    else{

    payload = {
        "email": Email.value,
        "password": Password.value
    }
    //console.log(payload);
    
    var request = new XMLHttpRequest();
    request.open('POST', 'http://127.0.0.1:8000/signup/');
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Accept', 'application/json');
    
    request.onload = function() {
        const status = request.status;

        if (status === 202) {
            window.location.replace("login.html");
        }
    }


    request.send(JSON.stringify(payload));
}

}
