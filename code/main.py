from typing import Union
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

app = FastAPI()

@app.get("/", response_model=home)
async def read_root():
    return {"mensaje": "API REST"}

@app.get("/clientes/", response_model=List[Cliente])
async def read_root():
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clientes')
        response = cursor.fetchall()
        return response

@app.get("/clientes/{id}", response_model=Cliente)
async def read_item(id: int):
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('select * from clientes where id_cliente = {};'.format(id))
            response = cursor.fetchone()
            return response
