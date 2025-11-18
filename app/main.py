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

# CORS Middleware - FIXED VERSION
# List your React dev server URL specifically
origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",  # Create React App default
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specific origins instead of ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # Add this line
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