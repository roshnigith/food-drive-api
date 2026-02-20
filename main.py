# main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FoodDrive table
class FoodDrive(Base):
    __tablename__ = "food_drives"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    city = Column(String, nullable=False, index=True)
    location = Column(String)
    food_type = Column(String)
    total_meals = Column(Integer, nullable=False)
    meals_distributed = Column(Integer, default=0)
    organizer_name = Column(String)
    contact_phone = Column(String)
    drive_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Distribution Drive API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class FoodDriveCreate(BaseModel):
    title: str
    description: str | None = None
    city: str
    location: str | None = None
    food_type: str | None = None
    total_meals: int
    organizer_name: str | None = None
    contact_phone: str | None = None
    drive_date: datetime

# POST endpoint to create a food drive
@app.post("/food-drives")
def create_drive(drive: FoodDriveCreate):
    db = next(get_db())
    db_drive = FoodDrive(**drive.dict())
    db.add(db_drive)
    db.commit()
    db.refresh(db_drive)
    return db_drive

# GET endpoint to fetch drives by city
@app.get("/food-drives")
def get_drives(city: str):
    db = next(get_db())
    drives = db.query(FoodDrive).filter(FoodDrive.city.ilike(city)).all()
    if not drives:
        raise HTTPException(status_code=404, detail="No drives found for this city")
    return drives
