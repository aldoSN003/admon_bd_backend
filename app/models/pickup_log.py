from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class PickupLog(Base):
    __tablename__ = "PickupLog"

    pickupLogId = Column(Integer, primary_key=True, autoincrement=True)
    studentId = Column(Integer, ForeignKey("Student.studentId", ondelete="CASCADE"), nullable=False)
    guardianId = Column(Integer, ForeignKey("Guardian.guardianId", ondelete="CASCADE"), nullable=False)
    pickupDateTime = Column(DateTime, default=datetime.now)
    faceMatchConfidence = Column(DECIMAL(5, 2))
    wasSuccessful = Column(Boolean, nullable=False)
    capturedPhotoUrl = Column(String(500))
    notes = Column(Text)

    # Relationships
    student = relationship("Student", back_populates="pickup_logs")
    guardian = relationship("Guardian", back_populates="pickup_logs")