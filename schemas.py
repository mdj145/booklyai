from pydantic import BaseModel, EmailStr
from datetime import datetime

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    business_name: str = ""

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AppointmentCreate(BaseModel):
    customer_name: str
    customer_phone: str
    start_time: datetime
    end_time: datetime
    notes: str = ""
    reminder_24h: bool = True
    reminder_1h: bool = True

class AppointmentOut(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    start_time: datetime
    end_time: datetime
    notes: str
    reminder_24h: bool
    reminder_1h: bool
    class Config:
        from_attributes = True
