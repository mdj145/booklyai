from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    business_name = Column(String, default="")
    timezone = Column(String, default="Europe/London")
    appointments = relationship("Appointment", back_populates="owner")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    notes = Column(Text, default="")
    reminder_24h = Column(Boolean, default=True)
    reminder_1h = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="appointments")
