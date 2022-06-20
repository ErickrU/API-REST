from urllib import response
from fastapi.testclient import TestClient

from code.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "API REST"}

def test_clientes():
    response = client.get("/clientes/")
    assert response.status_code == 200
    assert response.json() == [{"id_cliente":1,"nombre":"Erick","email":"Erick@gmail.com"},{"id_cliente":8,"nombre":"Mau","email":"Mau@gmail.com"},{"id_cliente":9,"nombre":"1","email":"Mau@gmail.com"},{"id_cliente":10,"nombre":"hello","email":"hello@test.com"}]

def test_clientes_1():
    response = client.get("/clientes/1")
    assert response.status_code == 200
    assert response.json() == {"id_cliente":1,"nombre":"Erick","email":"Erick@gmail.com"}

def test_add_post():
    data = {"nombre":"test","email":"test@test.com"}
    response = client.post("/clientes/", json=data)
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Cliente agregado"}

def test_update_put():
    data = {"id_cliente": 12,"nombre":"changed","email":"changed@changed.com"}
    response = client.put("/clientes/", json=data)
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Cliente actualizado"}

def test_remove_delete():
    response = client.delete("/clientes/12")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Cliente eliminado"} 

def test_clientes_outofrange():
    response = client.get("/clientes/100")
    assert response.status_code == 200
    assert response.json() == None

def test_not_found():
    response = client.get("/Ayuda")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}