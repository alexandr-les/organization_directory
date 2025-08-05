from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import organization as models
from app.schemas import organization as schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/organizations/", response_model=schemas.Organization)
def create_organization(org: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    db_building = db.query(models.Building).filter(models.Building.id == org.building_id).first()
    if not db_building:
        raise HTTPException(status_code=404, detail="Building not found")

    db_org = models.Organization(name=org.name, building_id=org.building_id)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)

    for phone_number in org.phone_numbers:
        db_phone = models.Phone(number=phone_number)
        db.add(db_phone)
        db.commit()
        db.refresh(db_phone)
        db_org.phones.append(db_phone)

    for activity_id in org.activity_ids:
        db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
        if db_activity:
            db_org.activities.append(db_activity)

    db.commit()
    db.refresh(db_org)
    return db_org

@router.get("/organizations/", response_model=List[schemas.Organization])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    organizations = db.query(models.Organization).offset(skip).limit(limit).all()
    return organizations

@router.get("/organizations/{organization_id}", response_model=schemas.Organization)
def read_organization(organization_id: int, db: Session = Depends(get_db)):
    db_organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization

@router.get("/organizations/by-building/{building_id}", response_model=List[schemas.Organization])
def get_organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    organizations = db.query(models.Organization).filter(models.Organization.building_id == building_id).all()
    return organizations

@router.get("/organizations/by-activity/{activity_id}", response_model=List[schemas.Organization])
def get_organizations_by_activity(activity_id: int, db: Session = Depends(get_db)):
    organizations = db.query(models.Organization).join(models.Organization.activities).filter(models.Activity.id == activity_id).all()
    return organizations

@router.get("/organizations/by-radius/", response_model=List[schemas.Organization])
def get_organizations_by_radius(latitude: float, longitude: float, radius: float, db: Session = Depends(get_db)):
    # Пример реализации поиска в радиусе
    # Здесь должна быть логика для поиска организаций в заданном радиусе
    organizations = db.query(models.Organization).all()
    return organizations
