from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables
from .api.routes import projects

app = FastAPI(
    title="AutoNomie API",
    description="Autonomous Development Agent Ecosystem",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(projects.router, prefix="/projects", tags=["projects"])