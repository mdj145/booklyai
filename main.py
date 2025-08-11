from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from .db import Base, engine, get_db
from .models import User, Appointment
from .schemas import AppointmentCreate, AppointmentOut
from .auth import router as auth_router

app = FastAPI(title="BooklyAI MVP")
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router)

# Serve static frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

# Simple current user: create demo user if none exists (MVP convenience)
def get_current_user(db: Session = Depends(get_db)) -> User:
    user = db.query(User).first()
    if not user:
        user = User(email="demo@bookly.ai", password_hash="demo", business_name="Demo Business")
        db.add(user); db.commit(); db.refresh(user)
    return user

# Create appointment
@app.post("/api/appointments", response_model=AppointmentOut)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    appt = Appointment(
        user_id=user.id,
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        start_time=payload.start_time,
        end_time=payload.end_time,
        notes=payload.notes,
        reminder_24h=payload.reminder_24h,
        reminder_1h=payload.reminder_1h,
    )
    db.add(appt); db.commit(); db.refresh(appt)
    return appt

# List appointments
@app.get("/api/appointments", response_model=List[AppointmentOut])
def list_appointments(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(Appointment).filter(Appointment.user_id == user.id).order_by(Appointment.start_time.desc()).all()
    return items

# Delete appointment
@app.delete("/api/appointments/{appt_id}")
def delete_appointment(appt_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    appt = db.query(Appointment).filter(Appointment.id == appt_id, Appointment.user_id == user.id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(appt); db.commit()
    return {"ok": True}
