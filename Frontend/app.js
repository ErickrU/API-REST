function getAll(){
    var request = new XMLHttpRequest();
    //Accede a la session de la pagina

    request.open('GET', "http://127.0.0.1:8000/clientes/");
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa("user" + ":" + "user"))
    request.setRequestHeader("content-type", "application/json");
    
    const  table   = document.getElementById("client_table");

    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");

    tblHead.innerHTML = `
        <a href="/post_cliente.html">
            <button>Agregar cliente</button>
        </a>
        <tr>            
            <th>ID Cliente</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Ver detalles</th>
            <th>Editar</th>
            <th>Eliminar</th>
        </tr>`;

    request.send();

    /*request.onload = () => {
        if(request.status === 202){
            console.log(JSON.parse(request.response))
        }else{
            console.log(JSON.parse(request.response))
            }
    }*/
    request.onload = () => {
        // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
        const response = request.responseText;
        const json = JSON.parse(response);
        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }
        else if (request.status == 202){
            const response = request.responseText;
            const json = JSON.parse(response);
            for (let i = 0; i < json.length; i++) {
                var tr = document.createElement('tr');
                var get_cliente = document.createElement('td');
                var idclt = document.createElement('td');
                var name = document.createElement('td');
                var email = document.createElement('td');
                var put_cliente = document.createElement('td');
                var delete_cleinte = document.createElement('td');

                get_cliente.innerHTML = "<a href=\get_cliente.html?"+json[i].id_cliente+">Detalle</a>";
                put_cliente.innerHTML = "<a href=\put_cliente.html?"+json[i].id_cliente+">Editar</a>";
                delete_cleinte.innerHTML = "<button onclick=deleteCliente("+json[i].id_cliente+")>Eliminar</button>";
                idclt.innerHTML = json[i].id_cliente;
                name.innerHTML = json[i].nombre;
                email.innerHTML = json[i].email;

                tr.appendChild(idclt);
                tr.appendChild(name);
                tr.appendChild(email);
                tr.appendChild(get_cliente);
                tr.appendChild(put_cliente);
                tr.appendChild(delete_cleinte);

                
                tblBody.appendChild(tr);
            }
            table.appendChild(tblHead);
            table.appendChild(tblBody);
        }
    };
    
}

function postCliente(){

    let nombre = document.getElementById("nombre");
    let email = document.getElementById("email");

    let payload = {
        "nombre": nombre.value,
        "email": email.value        
    }

    var request = new XMLHttpRequest();
    request.open('POST', 'http://localhost:8000/clientes/', true);
    request.setRequestHeader("Authorization", "Basic " + btoa("user:user"))
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Accept', 'application/json');

    request.onload = function() {
        const status = request.status;

        if (status === 202) {
            window.location.replace("index.html");
        }
    }

    request.send(JSON.stringify(payload));

}

function getCliente() {
    var id_cliente = window.location.search.substring(1);
    var request = new XMLHttpRequest();

    request.open('GET', 'http://localhost:8000/clientes/'+id_cliente);
    request.setRequestHeader("Authorization", "Basic " + btoa("user:user"))

    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);

        console.log("Response " + json);
        

        if (request.status == 202) {
            let nombre = document.getElementById("nombre");
            let email = document.getElementById("email");

            nombre.value = json.nombre;
            email.value = json.email;
        }

        else if(request.status == 401){
            alert(json.detail);
        }
    };
    request.send();

};

function putCliente(){

    console.log("putCliente");
    
    let id_cliente = window.location.search.substring(1);
    let nombre = document.getElementById("nombre");
    let email = document.getElementById("email");

    let payload = {

        "id_cliente": id_cliente,
        "nombre": nombre.value,
        "email": email.value        
    }

    var request = new XMLHttpRequest();
    request.open('PUT', 'http://localhost:8000/clientes/', true);
    request.setRequestHeader("Authorization", "Basic " + btoa("admin:admin"))
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Accept', 'application/json');

    request.onload = function() {
        const status = request.status;

        if (status === 202) {
            window.location.replace("index.html");
        }
    }

    request.send(JSON.stringify(payload));

}

function deleteCliente(id_cliente){
    console.log(id_cliente);
    let request = new XMLHttpRequest();

    request.open('DELETE', 'http://localhost:8000/clientes/'+id_cliente);
    request.setRequestHeader("Authorization", "Basic " + btoa("admin:admin"))

    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);

        if (request.status == 202) {
            location.reload();
        }

        else if(request.status == 401){
            alert(json.detail);
        }
    };
    request.send();

}