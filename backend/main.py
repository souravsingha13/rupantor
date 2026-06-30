from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.auth import router as auth_router
from db.database import Base, engine

from models.user import User

from core.config import settings

app = FastAPI(
    title="Salon Booking API",
    description="Backend API for Salon & Beauty Parlor Booking Application",
    version="1.0.0",
    debug=settings.DEBUG,
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Salon Booking API is running 🚀"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


# Register Routers


app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)
