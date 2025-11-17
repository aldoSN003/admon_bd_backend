from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import PickupLog, Student, Guardian
from app.schemas import (
    PickupLogCreate,
    PickupLogResponse
)

router = APIRouter(prefix="/pickup-logs", tags=["Pickup Logs"])


# CREATE - Register new pickup
@router.post("/", response_model=PickupLogResponse, status_code=status.HTTP_201_CREATED)
def create_pickup_log(pickup: PickupLogCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(Student).filter(Student.studentId == pickup.studentId).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if guardian exists
    guardian = db.query(Guardian).filter(Guardian.guardianId == pickup.guardianId).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found")

    # Create new pickup log
    db_pickup = PickupLog(
        studentId=pickup.studentId,
        guardianId=pickup.guardianId,
        wasSuccessful=pickup.wasSuccessful,
        faceMatchConfidence=pickup.faceMatchConfidence,
        capturedPhotoUrl=pickup.capturedPhotoUrl,
        notes=pickup.notes,
        pickupDateTime=datetime.now()
    )
    db.add(db_pickup)
    db.commit()
    db.refresh(db_pickup)
    return db_pickup


# READ - Get all pickup logs
@router.get("/", response_model=List[PickupLogResponse])
def get_pickup_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(PickupLog).order_by(PickupLog.pickupDateTime.desc()).offset(skip).limit(limit).all()
    return logs


# READ - Get pickup log by ID
@router.get("/{log_id}", response_model=PickupLogResponse)
def get_pickup_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(PickupLog).filter(PickupLog.pickupLogId == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Pickup log not found")
    return log


# READ - Get pickup logs by student
@router.get("/student/{student_id}", response_model=List[PickupLogResponse])
def get_pickup_logs_by_student(student_id: int, db: Session = Depends(get_db)):
    logs = db.query(PickupLog).filter(
        PickupLog.studentId == student_id
    ).order_by(PickupLog.pickupDateTime.desc()).all()
    return logs


# READ - Get pickup logs by guardian
@router.get("/guardian/{guardian_id}", response_model=List[PickupLogResponse])
def get_pickup_logs_by_guardian(guardian_id: int, db: Session = Depends(get_db)):
    logs = db.query(PickupLog).filter(
        PickupLog.guardianId == guardian_id
    ).order_by(PickupLog.pickupDateTime.desc()).all()
    return logs


# DELETE - Delete pickup log
@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pickup_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(PickupLog).filter(PickupLog.pickupLogId == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Pickup log not found")

    db.delete(log)
    db.commit()
    return None