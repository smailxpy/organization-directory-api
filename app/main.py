from fastapi import FastAPI
from app.routers import buildings, activities, organizations

app = FastAPI(title="Organization Directory API")

app.include_router(buildings.router)
app.include_router(activities.router)
app.include_router(organizations.router)

@app.get("/")
def root():
    return {"message": "Organization Directory API is running!"}
