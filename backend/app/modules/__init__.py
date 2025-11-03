"""
Domain/Feature Modules Package

This package contains all feature modules organized by domain.
Each module is self-contained with its own router, schemas, service, and models.
"""

from .auth import router as auth_router
from .resume import router as resume_router
from .jobs import router as jobs_router
from .interview import router as interview_router
from .footprint import router as footprint_router

__all__ = [
    "auth_router",
    "resume_router",
    "jobs_router",
    "interview_router",
    "footprint_router",
]
