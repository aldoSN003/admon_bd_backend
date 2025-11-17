from pydantic import BaseModel

# Schema for creating a student-guardian relationship
class StudentGuardianCreate(BaseModel):
    studentId: int
    guardianId: int
    relationship: str  # e.g., "padre", "madre", "tutor legal"

# Schema for response
class StudentGuardianResponse(BaseModel):
    studentId: int
    guardianId: int
    relationship: str

    class Config:
        from_attributes = True