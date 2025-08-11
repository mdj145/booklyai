from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
from .schemas import SignupRequest, LoginRequest
from .utils import hash_password, verify_password, create_jwt

router = APIRouter(prefix="/api/auth", tags=["auth"])
COOKIE_NAME = "booklyai_jwt"

def set_jwt_cookie(resp: JSONResponse, token: str):
    resp.set_cookie(key=COOKIE_NAME, value=token, httponly=True, samesite="lax")

@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=str(payload.email), password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    token = create_jwt({"user_id": user.id})
    resp = JSONResponse({"ok": True}); set_jwt_cookie(resp, token); return resp

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt({"user_id": user.id})
    resp = JSONResponse({"ok": True}); set_jwt_cookie(resp, token); return resp

@router.post("/logout")
def logout():
    resp = JSONResponse({"ok": True}); resp.delete_cookie(COOKIE_NAME); return resp
