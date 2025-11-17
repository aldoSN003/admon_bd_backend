from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import StudentGuardian, Student, Guardian
from app.schemas import (
    StudentGuardianCreate,
    StudentGuardianResponse
)

router = APIRouter(prefix="/student-guardians", tags=["Student-Guardian Relations"])


# CREATE - Assign guardian to student
@router.post("/", response_model=StudentGuardianResponse, status_code=status.HTTP_201_CREATED)
def create_student_guardian_relation(relation: StudentGuardianCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(Student).filter(Student.studentId == relation.studentId).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if guardian exists
    guardian = db.query(Guardian).filter(Guardian.guardianId == relation.guardianId).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found")

    # Check if relation already exists
    existing = db.query(StudentGuardian).filter(
        StudentGuardian.studentId == relation.studentId,
        StudentGuardian.guardianId == relation.guardianId
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create new relation
    db_relation = StudentGuardian(
        studentId=relation.studentId,
        guardianId=relation.guardianId,
        relationship_type=relation.relationship
    )
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation


# READ - Get all guardians for a student
@router.get("/student/{student_id}", response_model=List[StudentGuardianResponse])
def get_guardians_by_student(student_id: int, db: Session = Depends(get_db)):
    relations = db.query(StudentGuardian).filter(StudentGuardian.studentId == student_id).all()
    return relations


# READ - Get all students for a guardian
@router.get("/guardian/{guardian_id}", response_model=List[StudentGuardianResponse])
def get_students_by_guardian(guardian_id: int, db: Session = Depends(get_db)):
    relations = db.query(StudentGuardian).filter(StudentGuardian.guardianId == guardian_id).all()
    return relations


# DELETE - Remove guardian from student
@router.delete("/{student_id}/{guardian_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_guardian_relation(student_id: int, guardian_id: int, db: Session = Depends(get_db)):
    relation = db.query(StudentGuardian).filter(
        StudentGuardian.studentId == student_id,
        StudentGuardian.guardianId == guardian_id
    ).first()

    if not relation:
        raise HTTPException(status_code=404, detail="Relationship not found")

    db.delete(relation)
    db.commit()
    return None