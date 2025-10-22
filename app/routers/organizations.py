from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from math import radians, cos, sin, asin, sqrt
from app import models, database
from app.schemas.organization import Organization, OrganizationCreate
from app.utils.auth import verify_api_key  # ✅ add this line

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
    dependencies=[Depends(verify_api_key)]  
    )

# ----------------------------
# Basic CRUD
# ----------------------------

@router.get("/", response_model=list[Organization])
def get_organizations(db: Session = Depends(database.get_db)):
    return db.query(models.organization.Organization).all()


@router.post("/", response_model=Organization)
def create_organization(org: OrganizationCreate, db: Session = Depends(database.get_db)):
    new_org = models.organization.Organization(
        name=org.name,
        phone_numbers=org.phone_numbers,
        building_id=org.building_id,
    )
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    # Attach activities if provided
    if org.activity_ids:
        activities = db.query(models.activity.Activity).filter(
            models.activity.Activity.id.in_(org.activity_ids)
        ).all()
        new_org.activities.extend(activities)
        db.commit()
        db.refresh(new_org)

    return new_org


@router.get("/{org_id}", response_model=Organization)
def get_organization(org_id: int, db: Session = Depends(database.get_db)):
    org = db.query(models.organization.Organization).filter(
        models.organization.Organization.id == org_id
    ).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


# ----------------------------
# Filter: organizations in a building
# ----------------------------

@router.get("/building/{building_id}", response_model=list[Organization])
def get_orgs_by_building(building_id: int, db: Session = Depends(database.get_db)):
    orgs = db.query(models.organization.Organization).filter(
        models.organization.Organization.building_id == building_id
    ).all()
    return orgs


# ----------------------------
# Filter: organizations by activity (include nested)
# ----------------------------

def get_activity_children(activity, children=None):
    if children is None:
        children = []
    for child in activity.children:
        children.append(child)
        get_activity_children(child, children)
    return children


@router.get("/activity/{activity_id}", response_model=list[Organization])
def get_orgs_by_activity(activity_id: int, db: Session = Depends(database.get_db)):
    activity = db.query(models.activity.Activity).get(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    all_ids = [activity.id] + [a.id for a in get_activity_children(activity)]
    orgs = (
        db.query(models.organization.Organization)
        .join(models.organization.organization_activity)
        .filter(models.organization.organization_activity.c.activity_id.in_(all_ids))
        .all()
    )
    return orgs


# ----------------------------
# Filter: search by organization name
# ----------------------------

@router.get("/search", response_model=list[Organization])
def search_organizations(
    name: str = Query(..., description="Part of the organization name"),
    db: Session = Depends(database.get_db),
):
    orgs = (
        db.query(models.organization.Organization)
        .filter(models.organization.Organization.name.ilike(f"%{name}%"))
        .all()
    )
    return orgs


# ----------------------------
# Filter: organizations near coordinates (simple radius)
# ----------------------------

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


@router.get("/near", response_model=list[Organization])
def get_orgs_near(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius_km: float = Query(1.0, description="Search radius in kilometers"),
    db: Session = Depends(database.get_db),
):
    buildings = db.query(models.building.Building).all()
    nearby_buildings = [
        b.id for b in buildings if haversine(lat, lon, b.latitude, b.longitude) <= radius_km
    ]

    orgs = (
        db.query(models.organization.Organization)
        .filter(models.organization.Organization.building_id.in_(nearby_buildings))
        .all()
    )
    return orgs
