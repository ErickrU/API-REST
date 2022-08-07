function login(token){

    sessionStorage.setItem("token", token);

    var request = new XMLHttpRequest();
    request.open('GET', 'http://127.0.0.1:8000/user/');
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Accept', 'application/json');

    request.onload = function() {
        const status = request.status;
        console.log(status);
        if (status === 202) {
            window.location.replace("welcome.html");
        }
        else{
            sessionStorage.removeItem("token");
        }
    }

    request.send();
    
}

function getToken(){
    
    if (token = sessionStorage.getItem("token") == null){
        let Email = document.getElementById("Email");
        let Password = document.getElementById("Password");

        if (Email.value == "" || Password.value == ""){
            console.log("Empty fields");
        }
        else{

        var request = new XMLHttpRequest();
        request.open('GET', 'http://127.0.0.1:8000/user/validate/');
        request.setRequestHeader("Authorization", "Basic " + btoa(Email.value + ":" + Password.value));
        request.setRequestHeader('Content-Type', 'application/json');
        request.setRequestHeader('Accept', 'application/json');

        request.onload = function() {
            const status = request.status;

            if (status === 202) {
                token = request.responseText
                token = JSON.parse(token);
                token = token.token;
                login(token);
            }
        }

        request.send();
    }

    }
    else{
        token = sessionStorage.getItem("token");
        login(token);
    }

        
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
