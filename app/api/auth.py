from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.db.dependencies import get_db
from app.core.roles import ADMIN, DEVELOPER
import os
from dotenv import load_dotenv
from app.core.jwt import create_otp_token, verify_otp_token, create_access_token, hash_otp
import random

load_dotenv()

router = APIRouter(tags=["Auth"])

bearer_scheme = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


@router.post("/create_user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if user.role not in [ADMIN, DEVELOPER]:
        raise HTTPException(status_code=400, detail="Invalid role")

    db_user = User(
        name=user.name,
        email=user.email,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully"}

@router.post("/request-login")
def request_login(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp = str(random.randint(100000, 999999))

    hashed_otp = hash_otp(otp)

    otp_token = create_otp_token(email, hashed_otp)
    print(f"OTP for {email}: {otp}")

    return {
        "message": "OTP sent",
        "otp_token": otp_token  
    }

@router.post("/verify-login")
def verify_login(email: str, otp: str, otp_token: str, db: Session = Depends(get_db)):
    payload = verify_otp_token(otp_token)

    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    if payload["email"] != email:
        raise HTTPException(status_code=400, detail="Email mismatch")

    if payload["otp"] != hash_otp(otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token({
        "sub": user.email,
        "role": user.role,
        "user_id": user.id,
    })
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


@router.get("/test-auth")
def test_auth(current_user: User = Depends(get_current_user)):
    return {
        "message": "Authorized",
        "user": current_user.email,
        "role": current_user.role
    }


def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    total = db.query(User).count()
    users = db.query(User).offset(offset).limit(limit).all()
    return {"total": total, "limit": limit, "offset": offset, "users": users}
