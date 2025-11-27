from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Guardian(Base):
    __tablename__ = "Guardian"

    guardianId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(100), nullable=False)
    lastNamePaternal = Column(String(100), nullable=False)
    lastNameMaternal = Column(String(100))
    age = Column(Integer)
    phone = Column(String(15))
    email = Column(String(100), unique=True)
    password = Column(String(255), nullable=False)
    address = Column(String(255))
    photographUrl = Column(String(500))
    faceEncodingUrl = Column(String(500))
    lastUpdate = Column(DateTime)
    registrationDate = Column(DateTime, default=datetime.now)
    hasEmbedding = Column(Integer, default=0)  # 0 = No, 1 = Yes

    # Relationships
    students = relationship("StudentGuardian", back_populates="guardian")
    pickup_logs = relationship("PickupLog", back_populates="guardian")