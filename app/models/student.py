from sqlalchemy import Column, Integer, String, Date, CHAR
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    __tablename__ = "Student"

    studentId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(100), nullable=False)
    lastNamePaternal = Column(String(100), nullable=False)
    lastNameMaternal = Column(String(100))
    enrollmentNumber = Column(String(20), nullable=False, unique=True)
    birthDate = Column(Date)
    gender = Column(CHAR(1))
    grade = Column(String(50))
    groupName = Column(String(10))
    photographUrl = Column(String(500))

    # Relationships
    guardians = relationship("StudentGuardian", back_populates="student")
    pickup_logs = relationship("PickupLog", back_populates="student")