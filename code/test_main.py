from urllib import response
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "API REST"}

def test_clientes():
    response = client.get("/clientes/")
    assert response.status_code == 200
    assert response.json() == [
        {"id_cliente":1,"nombre":"Erick","email":"Erick@gmail.com"},
        {"id_cliente":2,"nombre":"Yael","email":"yael@gmail.com"},
        {"id_cliente":3,"nombre":"Michelle","email":"Michelle@gmail.com"}
        ]

def test_clientes_1():
    response = client.get("/clientes/1")
    assert response.status_code == 200
    assert response.json() == {"id_cliente":1,"nombre":"Erick","email":"Erick@gmail.com"}

def test_clientes_outofrange():
    response = client.get("/clientes/10")
    assert response.status_code == 200
    assert response.json() == None


def test_not_found():
    response = client.get("/Ayuda")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}