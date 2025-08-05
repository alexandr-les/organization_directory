from fastapi import FastAPI
from app.db.session import engine
from app.models import organization, building, activity
from app.api import organizations_router, buildings_router, activities_router

organization.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(organizations_router, prefix="/api/v1")
app.include_router(buildings_router, prefix="/api/v1")
app.include_router(activities_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Organization Directory API"}
