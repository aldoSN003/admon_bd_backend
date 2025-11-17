from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema with common fields
class AdministratorBase(BaseModel):
    firstName: str
    lastNamePaternal: str
    lastNameMaternal: Optional[str] = None
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

# Schema for creating an administrator
class AdministratorCreate(AdministratorBase):
    password: str

# Schema for updating an administrator
class AdministratorUpdate(BaseModel):
    firstName: Optional[str] = None
    lastNamePaternal: Optional[str] = None
    lastNameMaternal: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

# Schema for login
class AdministratorLogin(BaseModel):
    username: str
    password: str

# Schema for response (without password)
class AdministratorResponse(AdministratorBase):
    administratorId: int

    class Config:
        from_attributes = True