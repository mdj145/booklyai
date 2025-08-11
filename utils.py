import os, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "48"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_jwt(payload: dict) -> str:
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {**payload, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
