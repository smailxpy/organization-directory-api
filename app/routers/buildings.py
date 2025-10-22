from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from app.schemas.building import Building, BuildingCreate
from app.utils.auth import verify_api_key

router = APIRouter(prefix="/buildings", tags=["Buildings"])

# Get all buildings
@router.get("/", response_model=list[Building])
def get_buildings(db: Session = Depends(database.get_db)):
    buildings = db.query(models.building.Building).all()
    return buildings

# Create a new building
@router.post("/", response_model=Building)
def create_building(building: BuildingCreate, db: Session = Depends(database.get_db)):
    new_building = models.building.Building(**building.dict())
    db.add(new_building)
    db.commit()
    db.refresh(new_building)
    return new_building

router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
    dependencies=[Depends(verify_api_key)]
)
