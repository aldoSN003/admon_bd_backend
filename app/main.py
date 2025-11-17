from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routes import administrator, guardian, student, student_guardian, pickup_log

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS Middleware (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(administrator.router)
app.include_router(guardian.router)
app.include_router(student.router)
app.include_router(student_guardian.router)
app.include_router(pickup_log.router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to GuardianFace API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}