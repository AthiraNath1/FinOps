from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
import jwt
import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from router.integration.db_operation import db_integration
from core_dependencies.database import get_db
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

router = APIRouter(
    tags=["Auth API"]
)
SECRET_KEY = 'your-secret-key'
# Dummy user for example
USERS = {'ath@example.com': 'password123'}

class LoginRequest(BaseModel):
    email: str

class TokenResponse(BaseModel):
    token: str

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest,db=Depends(get_db)):
    email = request.email
    x=db_integration.get_user(db=db, user_email=email)

    if email == x[0].user_email:
        token = jwt.encode({
            'user': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def decode_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")





security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
