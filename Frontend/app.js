function getAll(){
    var request = new XMLHttpRequest();
    //Accede a la session de la pagina
    username = window.prompt('Username:')
    password = window.prompt('Password:')

    request.open('GET', "http://127.0.0.1:8000/clientes/");
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("content-type", "application/json");
    
    const  table   = document.getElementById("client_table");

    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");

    tblHead.innerHTML = `
        <tr>
            <th>ID Cliente</th>
            <th>Nombre</th>
            <th>Email</th>
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
                var idclt = document.createElement('td');
                var name = document.createElement('td');
                var email = document.createElement('td');

                idclt.innerHTML = json[i].id_cliente;
                name.innerHTML = json[i].nombre;
                email.innerHTML = json[i].email;

                tr.appendChild(idclt);
                tr.appendChild(name);
                tr.appendChild(email);
                
                tblBody.appendChild(tr);
            }
            table.appendChild(tblHead);
            table.appendChild(tblBody);
        }
    };
    
}