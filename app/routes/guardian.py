from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from datetime import datetime

from app.database import get_db
from app.models import Guardian
from app.schemas import (
    GuardianCreate,
    GuardianUpdate,
    GuardianLogin,
    GuardianResponse
)

router = APIRouter(prefix="/guardians", tags=["Guardians"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# CREATE - Register new guardian
@router.post("/", response_model=GuardianResponse, status_code=status.HTTP_201_CREATED)
def create_guardian(guardian: GuardianCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(Guardian).filter(Guardian.email == guardian.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(guardian.password)

    # Create new guardian
    db_guardian = Guardian(
        firstName=guardian.firstName,
        lastNamePaternal=guardian.lastNamePaternal,
        lastNameMaternal=guardian.lastNameMaternal,
        age=guardian.age,
        phone=guardian.phone,
        email=guardian.email,
        password=hashed_password,
        address=guardian.address,
        lastUpdate=datetime.now(),
        registrationDate=datetime.now()
    )
    db.add(db_guardian)
    db.commit()
    db.refresh(db_guardian)
    return db_guardian


# READ - Get all guardians
@router.get("/", response_model=List[GuardianResponse])
def get_guardians(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    guardians = db.query(Guardian).offset(skip).limit(limit).all()
    return guardians


# READ - Get guardian by ID
@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_guardian(guardian_id: int, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.guardianId == guardian_id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return guardian


# UPDATE - Update guardian
@router.put("/{guardian_id}", response_model=GuardianResponse)
def update_guardian(guardian_id: int, guardian_update: GuardianUpdate, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.guardianId == guardian_id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found")

    # Update fields if provided
    update_data = guardian_update.model_dump(exclude_unset=True)

    # Hash password if provided
    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"])

    for key, value in update_data.items():
        setattr(guardian, key, value)

    guardian.lastUpdate = datetime.now()

    db.commit()
    db.refresh(guardian)
    return guardian


# DELETE - Delete guardian
@router.delete("/{guardian_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guardian(guardian_id: int, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.guardianId == guardian_id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found")

    db.delete(guardian)
    db.commit()
    return None


# LOGIN - Authenticate guardian
@router.post("/login")
def login_guardian(credentials: GuardianLogin, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.email == credentials.email).first()

    if not guardian or not pwd_context.verify(credentials.password, guardian.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "guardian": GuardianResponse.model_validate(guardian)
    }