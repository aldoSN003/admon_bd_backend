from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class StudentGuardian(Base):
    __tablename__ = "StudentGuardian"

    studentId = Column(Integer, ForeignKey("Student.studentId", ondelete="CASCADE"), primary_key=True)
    guardianId = Column(Integer, ForeignKey("Guardian.guardianId", ondelete="CASCADE"), primary_key=True)
    relationship_type = Column("relationship", String(50), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="guardians")
    guardian = relationship("Guardian", back_populates="students")