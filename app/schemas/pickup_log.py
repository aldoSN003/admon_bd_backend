from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

# Base schema
class PickupLogBase(BaseModel):
    studentId: int
    guardianId: int
    wasSuccessful: bool
    faceMatchConfidence: Optional[Decimal] = None
    capturedPhotoUrl: Optional[str] = None
    notes: Optional[str] = None

# Schema for creating a pickup log
class PickupLogCreate(PickupLogBase):
    pass

# Schema for response
class PickupLogResponse(PickupLogBase):
    pickupLogId: int
    pickupDateTime: datetime

    class Config:
        from_attributes = True