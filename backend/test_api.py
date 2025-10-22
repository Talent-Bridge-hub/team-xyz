"""
Simple FastAPI test server - Standalone version
Test the API without complex imports
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

app = FastAPI(
    title="UtopiaHire API",
    description="AI-Powered Career Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
try:
    from backend.app.api.auth import router as auth_router
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
    print("✅ Authentication router loaded")
except Exception as e:
    print(f"⚠️  Authentication router failed to load: {e}")

try:
    from backend.app.api.resume import router as resume_router
    app.include_router(resume_router, prefix="/api/v1/resume", tags=["Resume"])
    print("✅ Resume router loaded")
except Exception as e:
    print(f"⚠️  Resume router failed to load: {e}")

try:
    from backend.app.api.jobs import router as jobs_router
    app.include_router(jobs_router)  # Prefix already in router
    print("✅ Jobs router loaded")
except Exception as e:
    print(f"⚠️  Jobs router failed to load: {e}")

try:
    from backend.app.api.interview import router as interview_router
    app.include_router(interview_router)  # Prefix already in router
    print("✅ Interview router loaded")
except Exception as e:
    print(f"⚠️  Interview router failed to load: {e}")

try:
    from backend.app.api.footprint import router as footprint_router
    app.include_router(footprint_router)  # Prefix already in router
    print("✅ Footprint router loaded")
except Exception as e:
    print(f"⚠️  Footprint router failed to load: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to UtopiaHire API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/v1/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "API is working!",
        "modules": [
            "Resume Reviewer",
            "Job Matcher",
            "Interview Simulator",
            "Footprint Scanner"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
