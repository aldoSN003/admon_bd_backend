from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from app.database import get_db
from app.models import Administrator
from app.schemas import (
    AdministratorCreate,
    AdministratorUpdate,
    AdministratorLogin,
    AdministratorResponse
)

router = APIRouter(prefix="/administrators", tags=["Administrators"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# CREATE - Register new administrator
@router.post("/", response_model=AdministratorResponse, status_code=status.HTTP_201_CREATED)
def create_administrator(admin: AdministratorCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(Administrator).filter(Administrator.username == admin.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash password
    hashed_password = pwd_context.hash(admin.password)

    # Create new administrator
    db_admin = Administrator(
        firstName=admin.firstName,
        lastNamePaternal=admin.lastNamePaternal,
        lastNameMaternal=admin.lastNameMaternal,
        username=admin.username,
        password=hashed_password,
        email=admin.email,
        phone=admin.phone
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


# READ - Get all administrators
@router.get("/", response_model=List[AdministratorResponse])
def get_administrators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    administrators = db.query(Administrator).offset(skip).limit(limit).all()
    return administrators


# READ - Get administrator by ID
@router.get("/{administrator_id}", response_model=AdministratorResponse)
def get_administrator(administrator_id: int, db: Session = Depends(get_db)):
    admin = db.query(Administrator).filter(Administrator.administratorId == administrator_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrator not found")
    return admin


# UPDATE - Update administrator
@router.put("/{administrator_id}", response_model=AdministratorResponse)
def update_administrator(administrator_id: int, admin_update: AdministratorUpdate, db: Session = Depends(get_db)):
    admin = db.query(Administrator).filter(Administrator.administratorId == administrator_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrator not found")

    # Update fields if provided
    update_data = admin_update.model_dump(exclude_unset=True)

    # Hash password if provided
    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"])

    for key, value in update_data.items():
        setattr(admin, key, value)

    db.commit()
    db.refresh(admin)
    return admin


# DELETE - Delete administrator
@router.delete("/{administrator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_administrator(administrator_id: int, db: Session = Depends(get_db)):
    admin = db.query(Administrator).filter(Administrator.administratorId == administrator_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrator not found")

    db.delete(admin)
    db.commit()
    return None


# LOGIN - Authenticate administrator
@router.post("/login")
def login_administrator(credentials: AdministratorLogin, db: Session = Depends(get_db)):
    admin = db.query(Administrator).filter(Administrator.username == credentials.username).first()
    
    if not admin or not pwd_context.verify(credentials.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "message": "Login successful",
        "administrator": AdministratorResponse.model_validate(admin)
    }