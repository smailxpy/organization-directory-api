from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from app.schemas.activity import Activity, ActivityCreate
from app.utils.auth import verify_api_key

router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
    dependencies=[Depends(verify_api_key)]
)

# Get all activities
@router.get("/", response_model=list[Activity])
def get_activities(db: Session = Depends(database.get_db)):
    return db.query(models.activity.Activity).all()

# Create an activity
@router.post("/", response_model=Activity)
def create_activity(activity: ActivityCreate, db: Session = Depends(database.get_db)):
    new_activity = models.activity.Activity(**activity.dict())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity
