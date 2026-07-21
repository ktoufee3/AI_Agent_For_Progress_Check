#api/app.py
from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="SMS Progress Checker Agent",
    description="AI Agent for Student Management System Progress Tracking",
    version="1.0.0"
)

app.include_router(router)