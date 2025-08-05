from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import activity as models
from app.schemas import activity as schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/activities/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.get("/activities/", response_model=List[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    activities = db.query(models.Activity).offset(skip).limit(limit).all()
    return activities

@router.get("/activities/{activity_id}", response_model=schemas.Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@router.get("/activities/{activity_id}/organizations", response_model=List[schemas.Activity])
def get_organizations_by_activity_with_subactivities(activity_id: int, db: Session = Depends(get_db)):
    # Получаем все подвиды деятельности
    subactivity_ids = [activity_id]
    activities = db.query(models.Activity).filter(models.Activity.parent_id == activity_id).all()
    for activity in activities:
        subactivity_ids.append(activity.id)
        sub_subactivities = db.query(models.Activity).filter(models.Activity.parent_id == activity.id).all()
        for sub_activity in sub_subactivities:
            subactivity_ids.append(sub_activity.id)
    
    organizations = db.query(models.Organization).join(models.Organization.activities).filter(models.Activity.id.in_(subactivity_ids)).all()
    return organizations
