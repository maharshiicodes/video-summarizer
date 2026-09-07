from fastapi import APIRouter,Depends,HTTPException,Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import uuid
from passlib.context import CryptContext
from video_summarizer.db.database import get_db
from video_summarizer.db.models import User
from video_summarizer.auth.jwt import create_access_token
router = APIRouter()
pwd_context = CryptContext(schemes = ["bcrypt"] , deprecated = "auto")

class RegisterRequest(BaseModel):
    name : str
    email : EmailStr
    password : str

class LoginRequest(BaseModel):
    email : EmailStr
    password : str


def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password[:72], hashed)

def set_auth_cookie(response : Response , token : str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age= 60 * 60 * 48
    )

@router.post("/register")
def register(request : RegisterRequest , response : Response , db : Session = Depends(get_db)):
    existing  = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code = 400 , detail = "email already exist")

    user = User(
        id = str(uuid.uuid4()),
        name = request.name,
        email = request.email,
        hashed_password = hash_password(request.password)
    )

    db.add(user)
    db.commit()

    token = create_access_token(user.id)
    set_auth_cookie(response,token)
    return {"id" : user.id , "name" : user.name , "email" : user.email}

@router.post("/login")
def login(request : LoginRequest , response : Response , db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password,user.hashed_password):
        raise HTTPException(status_code = 401 , detail = "invalid email address or password")

    access_token = create_access_token(user.id)
    set_auth_cookie(response,access_token)
    return {"id" : user.id , "name" : user.name , "email" : user.email}

@router.post("/logout")
def logout(response:Response):
    response.delete_cookie("access_token")
    return {"message" : "logged out"}