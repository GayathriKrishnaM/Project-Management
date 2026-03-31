from sqlalchemy.orm import Session
from app.models.user import User
from app.core.roles import ADMIN
import os
from dotenv import load_dotenv

load_dotenv()

def create_default_admin(db: Session):
    admin_email = os.getenv("admin_email")

    existing_admin = db.query(User).filter(User.email == admin_email).first()

    if not existing_admin:
        admin = User(
            name="Admin",
            email=admin_email,
            role=ADMIN
        )
        db.add(admin)
        db.commit()
        print("Default admin created")
    else:
        print("Default admin already exists")