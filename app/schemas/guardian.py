from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Base schema with common fields
class GuardianBase(BaseModel):
    firstName: str
    lastNamePaternal: str
    lastNameMaternal: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None

# Schema for creating a guardian
class GuardianCreate(GuardianBase):
    password: str

# Schema for updating a guardian
class GuardianUpdate(BaseModel):
    firstName: Optional[str] = None
    lastNamePaternal: Optional[str] = None
    lastNameMaternal: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    password: Optional[str] = None
    photographUrl: Optional[str] = None
    faceEncodingUrl: Optional[str] = None

# Schema for login
class GuardianLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for response (without password)
class GuardianResponse(GuardianBase):
    guardianId: int
    photographUrl: Optional[str] = None
    faceEncodingUrl: Optional[str] = None
    lastUpdate: Optional[datetime] = None
    registrationDate: Optional[datetime] = None

    class Config:
        from_attributes = True