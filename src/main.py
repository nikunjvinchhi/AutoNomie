from fastapi import FastAPI

app = FastAPI(
    title="AutoNomie API",
    description="Autonomous Development Agent Ecosystem",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "AutoNomie API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}