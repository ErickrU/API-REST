from lib2to3.pytree import Base
from typing import Union
from typing_extensions import Self
from urllib import response
from urllib.request import Request
from fastapi import Depends, FastAPI, HTTPException, status
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import sqlite3
import os
import hashlib
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status, Depends, Security, Request
from fastapi.responses import RedirectResponse
import pyrebase
from http import HTTPStatus

DATABASE_URL = os.path.join("code/sql/proyecto.sqlite")

class Usuarios(BaseModel):
    username: str
    level: int

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

class clientesSignup(BaseModel):
    email: str
    password: str


app = FastAPI()

security = HTTPBasic()

origins = [
    "http://localhost:8080",
    "http://0.0.0.0:8080",
    "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebaseConfig = {
    "apiKey": "AIzaSyCTVRE5UN_6skjR33-c2HwKu9NBv_0oeag",
    "authDomain": "fir-db-c676a.firebaseapp.com",
    "databaseURL": "https://fir-db-c676a-default-rtdb.firebaseio.com",
    "projectId": "fir-db-c676a",
    "storageBucket": "fir-db-c676a.appspot.com",
    "messagingSenderId": "423723094858",
    "appId": "1:423723094858:web:d73300d2db41754f6867b3",
    "measurementId": "G-VGGS1KJQ38"
  };

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

'''def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]'''

@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get token for a user",
    description="Get token for a user",
    tags=["Auth"],
  )
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
      user = credentials.username
      password = credentials.password
      user = auth.sign_in_with_email_and_password(user, password)
      response = {
        "token": user['idToken'],
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@app.get(
  "/user/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Login user and get user level",
  description="Login user and get user level",
  tags=["Auth"],
)
async def get_token_bearer(credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    try:
      user = auth.get_account_info(credentials.credentials)
      uid = user['users'][0]['localId']
      users_data = db.child("users").child(uid).get().val()
      response = {
        "user": users_data,
      }
      return response
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      

@app.post(
  "/signup/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Create a user",
  description="create a user",
  tags=["Auth"],
)
async def create_user_post(cliente: clientesSignup):
    try:
      user = auth.create_user_with_email_and_password(cliente.email, cliente.password)
      userI = auth.get_account_info(user['idToken'])
      uid = userI['users'][0]['localId']
      db.child("users").child(uid).set({"email": cliente.email, "nivel": "1"})

      response = {
        "message": "User created successfully",
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.get("/clientes/", response_model=List[Cliente], status_code=status.HTTP_202_ACCEPTED,summary="Regresa una lista de usuarios",description="Regresa una lista de usuarios",tags=["CRUD"])
async def read_all_items(credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    users_data = int(db.child("users").child(uid).child("nivel").get().val())
    if users_data == 1: #Para admin
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id}", response_model=Cliente,status_code=status.HTTP_202_ACCEPTED,summary="Regresa un cliente basandoso en un id dado",description="Regresa un cliente basandoso en un id dado",tags=["CRUD"])
async def read_an_item(id: int, credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    users_data = int(db.child("users").child(uid).child("nivel").get().val())
    if users_data == 1:
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('select * from clientes where id_cliente = {};'.format(id))
            response = cursor.fetchone()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/clientes/", response_model=respuestas,status_code=status.HTTP_202_ACCEPTED,summary="Agrega un cliente necesita nombre y email",description="Agrega un cliente necesita nombre y email",tags=["CRUD"])
async def add_an_item(cliente: clientesNE, credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    users_data = int(db.child("users").child(uid).child("nivel").get().val())
    if users_data == 1:
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('insert into clientes(nombre, email) values ("{}","{}");'.format(cliente.nombre,cliente.email))
            connection.commit()
            response = {
                "mensaje": "Cliente agregado"
            }
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )
    
@app.put("/clientes/", response_model=respuestas,status_code=status.HTTP_202_ACCEPTED,summary="Actualizar los datos de un cliente",description="Actualizar los datos de un cliente",tags=["CRUD"])
async def update_an_item(cliente: Cliente, credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    users_data = int(db.child("users").child(uid).child("nivel").get().val())
    if users_data == 1: #Administrador
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('update clientes set nombre = "{}", email = "{}" where id_cliente = {};'.format(cliente.nombre,cliente.email,cliente.id_cliente))
            connection.commit()
            response = {
                "mensaje": "Cliente actualizado"
            }
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete("/clientes/{id}",response_model=respuestas, status_code=status.HTTP_202_ACCEPTED,summary="Borrar un cliente por su id",description="Borrar un cliente por su id",tags=["CRUD"])
async def delete_an_item(id:int ,credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    users_data = int(db.child("users").child(uid).child("nivel").get().val())
    if users_data == 1: #Administrador
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('delete from clientes where id_cliente = {}'.format(id))
            connection.commit()
            response = {
                "mensaje": "Cliente eliminado"
            } 
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )