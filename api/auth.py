from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
import mysql.connector

from api.config import DATABASE_CONFIG

SECRET_KEY = "Snacktify-Secret-Key-Mastered"
ALGORITHM = "HS256"

router = APIRouter()
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials.scheme == "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    decoded_token = decode_access_token(credentials.credentials)
    return decoded_token


class RegisterRequest(BaseModel):
    email: str
    password: str
    repeat_password: str


class LoginRequest(BaseModel):
    email: str
    password: str


def get_db_connection():
    return mysql.connector.connect(**DATABASE_CONFIG)


@router.post("/register")
def register_user(request: RegisterRequest):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (request.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail = "User already exists")

    if request.password != request.repeat_password:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail = "Passwords do not match")

    hashed_password = hash_password(request.password)
    insert_query = "INSERT INTO users (email, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (request.email, hashed_password))

    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(request: LoginRequest):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (request.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        if verify_password(request.password, existing_user[1]):
            access_token = create_access_token({"sub": request.email})
            cursor.close()
            connection.close()
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=401, detail="Invalid credentials")

    cursor.close()
    connection.close()
    raise HTTPException(status_code=401, detail="User not found")
