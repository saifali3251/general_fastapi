from fastapi import FastAPI
# from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from db.session import create_tables

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)


@app.on_event("startup")
async def startup_event():
    create_tables()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}