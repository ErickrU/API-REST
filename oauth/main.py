from urllib import response
from fastapi import FastAPI, HTTPException, status, Depends, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import hashlib
from pydantic import BaseModel
import pyrebase

app = FastAPI()

origins = ["*"
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

class clientesNE(BaseModel):
    email: str
    password: str

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')

@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="log in",
    description="log in",
    tags=["auth"],
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
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

@app.get(
  "/user/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Get a token for a user",
  description="Get a token for a user",
  tags=["auth"],
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
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

@app.post(
  "/signup/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Create a user",
  description="create a user",
  tags=["auth"],
)
async def create_user_post(cliente: clientesNE):
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
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

