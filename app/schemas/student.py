from pydantic import BaseModel
from typing import Optional
from datetime import date

# Base schema with common fields
class StudentBase(BaseModel):
    firstName: str
    lastNamePaternal: str
    lastNameMaternal: Optional[str] = None
    enrollmentNumber: str
    birthDate: Optional[date] = None
    gender: Optional[str] = None
    grade: Optional[str] = None
    groupName: Optional[str] = None

# Schema for creating a student
class StudentCreate(StudentBase):
    pass

# Schema for updating a student
class StudentUpdate(BaseModel):
    firstName: Optional[str] = None
    lastNamePaternal: Optional[str] = None
    lastNameMaternal: Optional[str] = None
    enrollmentNumber: Optional[str] = None
    birthDate: Optional[date] = None
    gender: Optional[str] = None
    grade: Optional[str] = None
    groupName: Optional[str] = None
    photographUrl: Optional[str] = None

# Schema for response
class StudentResponse(StudentBase):
    studentId: int
    photographUrl: Optional[str] = None

    class Config:
        from_attributes = True