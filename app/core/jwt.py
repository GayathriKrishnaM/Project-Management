from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def hash_otp(otp: str):
    return hashlib.sha256(otp.encode()).hexdigest()

def create_otp_token(email: str, otp: str):
    payload = {
        "email": email,
        "otp": otp,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        "type": "otp"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_otp_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "otp":
            return None

        return payload
    except JWTError:
        return None


def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=2)
    payload["type"] = "access"

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

