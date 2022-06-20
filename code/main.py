from lib2to3.pytree import Base
from typing import Union
from typing_extensions import Self
from urllib import response
from urllib.request import Request
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import sqlite3

class home(BaseModel):
    mensaje: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class respuestas(BaseModel):
    mensaje: str

class clientesNE(BaseModel):
    nombre: str
    email: str

app = FastAPI()

@app.get("/", response_model=home)
async def read_root():
    return {"mensaje": "API REST"}

@app.get("/clientes/", response_model=List[Cliente])
async def read_all_items():
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clientes')
        response = cursor.fetchall()
        return response

@app.get("/clientes/{id}", response_model=Cliente)
async def read_an_item(id: int):
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('select * from clientes where id_cliente = {};'.format(id))
        response = cursor.fetchone()
        return response

@app.post("/clientes/", response_model=respuestas)
async def add_an_item(cliente: clientesNE):
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute('insert into clientes(nombre, email) values ("{}","{}");'.format(cliente.nombre,cliente.email))
        connection.commit()
        response = {
            "mensaje": "Cliente agregado"
        }
        return response
    
@app.put("/clientes/", response_model=respuestas)
async def update_an_item(cliente: Cliente):
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute('update clientes set nombre = "{}", email = "{}" where id_cliente = {};'.format(cliente.nombre,cliente.email,cliente.id_cliente))
        connection.commit()
        response = {
            "mensaje": "Cliente actualizado"
        }
        return response

@app.delete("/clientes/{id}", response_model=respuestas)
async def delete_an_item(id: int):
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute('delete from clientes where id_cliente = {}'.format(id))
        connection.commit()
        response = {
            "mensaje": "Cliente eliminado"
        }
        return response