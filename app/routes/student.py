from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Student
from app.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

router = APIRouter(prefix="/students", tags=["Students"])


# CREATE - Register new student
@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if enrollment number already exists
    existing = db.query(Student).filter(Student.enrollmentNumber == student.enrollmentNumber).first()
    if existing:
        raise HTTPException(status_code=400, detail="Enrollment number already registered")

    # Create new student
    db_student = Student(
        firstName=student.firstName,
        lastNamePaternal=student.lastNamePaternal,
        lastNameMaternal=student.lastNameMaternal,
        enrollmentNumber=student.enrollmentNumber,
        birthDate=student.birthDate,
        gender=student.gender,
        grade=student.grade,
        groupName=student.groupName
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# READ - Get all students
@router.get("/", response_model=List[StudentResponse])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


# READ - Get student by ID
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.studentId == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# READ - Get student by enrollment number
@router.get("/enrollment/{enrollment_number}", response_model=StudentResponse)
def get_student_by_enrollment(enrollment_number: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.enrollmentNumber == enrollment_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# UPDATE - Update student
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.studentId == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update fields if provided
    update_data = student_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


# DELETE - Delete student
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.studentId == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return None