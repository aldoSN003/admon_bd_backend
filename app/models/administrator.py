from sqlalchemy import Column, Integer, String
from app.database import Base


class Administrator(Base):
    __tablename__ = "Administrator"

    administratorId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(100), nullable=False)
    lastNamePaternal = Column(String(100), nullable=False)
    lastNameMaternal = Column(String(100))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100))
    phone = Column(String(15))