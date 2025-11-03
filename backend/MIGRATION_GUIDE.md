# Migration Guide: Domain-Based Architecture

> **Step-by-step guide to migrate from layer-based to domain-based architecture**

## 🎯 Migration Overview

**From:** Technical layers (api/, models/, core/)  
**To:** Domain modules (modules/auth/, modules/resume/, etc.)

**Status:** ✅ Structure created, ⚠️ Migration in progress

---

## 📋 Current State

### ✅ Completed:
- [x] New directory structure created
- [x] Files copied to new locations
- [x] Architecture documentation written
- [x] Module __init__.py files created

### ⚠️ In Progress:
- [ ] Update imports in all files
- [ ] Update main.py to use new routers
- [ ] Update tests
- [ ] Remove old structure

---

## 🔄 Migration Steps

### Step 1: Update Module Routers

Each module's `router.py` needs to be updated to export a router instance.

#### Example: Auth Module

**File:** `backend/app/modules/auth/router.py`

```python
# Add this at the top
from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreate, UserLogin, Token
from .service import AuthService
from shared.dependencies import get_current_user

# Create router instance
router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# Keep existing endpoints, just update imports
@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, service: AuthService = Depends()):
    """Register a new user"""
    return await service.register(user)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, service: AuthService = Depends()):
    """Login and get access token"""
    return await service.login(credentials)
```

**Repeat for:**
- `modules/resume/router.py`
- `modules/jobs/router.py`
- `modules/interview/router.py`
- `modules/footprint/router.py`

---

### Step 2: Update Module __init__.py

Each module needs to export its router.

#### Example: Auth Module

**File:** `backend/app/modules/auth/__init__.py`

```python
"""
Authentication Module

Handles user registration, login, and JWT token management.
"""

from .router import router

__all__ = ["router"]
```

**Repeat for all modules.**

---

### Step 3: Update Shared Module

Move common dependencies to `shared/`.

**File:** `backend/app/shared/dependencies.py`

```python
"""
Shared Dependencies

Common dependencies used across multiple modules.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get the current authenticated user.
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_db():
    """Database session dependency"""
    from .database import get_database_connection
    db = get_database_connection()
    try:
        yield db
    finally:
        db.close()
```

---

### Step 4: Update main.py

Update the main application to use new module routers.

**File:** `backend/app/main.py`

```python
"""
UtopiaHire Backend Application

Main FastAPI application with domain-based architecture.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.events import startup_event, shutdown_event

# Import module routers
from modules import (
    auth_router,
    resume_router,
    jobs_router,
    interview_router,
    footprint_router,
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Career Platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register startup/shutdown events
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# Include module routers
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(interview_router)
app.include_router(footprint_router)

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
```

---

### Step 5: Update Core Events

**File:** `backend/app/core/events.py`

```python
"""
Application Lifecycle Events

Startup and shutdown event handlers.
"""

import logging
from shared.database import init_database, close_database

logger = logging.getLogger(__name__)

async def startup_event():
    """
    Actions to perform on application startup.
    """
    logger.info("🚀 Starting UtopiaHire Backend...")
    
    # Initialize database connection
    await init_database()
    logger.info("✅ Database connected")
    
    # Initialize AI models
    # (Add your AI model initialization here)
    
    logger.info("✅ Application startup complete")

async def shutdown_event():
    """
    Actions to perform on application shutdown.
    """
    logger.info("🛑 Shutting down UtopiaHire Backend...")
    
    # Close database connection
    await close_database()
    logger.info("✅ Database connection closed")
    
    logger.info("✅ Application shutdown complete")
```

---

### Step 6: Update Import Statements

Update all imports to use new paths:

**Old:**
```python
from app.api.auth import router
from app.models.user import User
from app.core.security import hash_password
```

**New:**
```python
from modules.auth.router import router
from modules.auth.models import User
from shared.security import hash_password
```

---

### Step 7: Update Tests

Update test imports to use new structure:

**Old:**
```python
# tests/test_auth.py
from app.api.auth import router
```

**New:**
```python
# tests/modules/test_auth.py
from modules.auth.router import router
```

Create test directory structure:
```bash
tests/
├── modules/
│   ├── test_auth.py
│   ├── test_resume.py
│   ├── test_jobs.py
│   ├── test_interview.py
│   └── test_footprint.py
├── shared/
│   ├── test_security.py
│   └── test_database.py
└── integration/
    └── test_api_flow.py
```

---

### Step 8: Cleanup Old Structure

Once everything is working with the new structure:

```bash
cd backend/app

# Backup old structure
mkdir -p ../backup
mv api ../backup/
mv models ../backup/

# Remove old core files (config.py stays)
rm core/database.py
rm core/security.py
```

---

## ✅ Verification Checklist

After migration, verify:

- [ ] Backend starts without errors
- [ ] All API endpoints work (`/docs` page loads)
- [ ] Authentication flow works
- [ ] Database connections work
- [ ] All modules are accessible
- [ ] Tests pass
- [ ] No import errors

---

## 🧪 Testing the Migration

### 1. Start the Backend
```bash
cd backend
./start.sh
```

### 2. Check API Documentation
Visit: http://localhost:8000/docs

Verify all endpoints appear with proper tags:
- Authentication
- Resume
- Jobs
- Interview
- Footprint

### 3. Test Each Module
```bash
# Auth
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Resume
curl http://localhost:8000/api/v1/resumes/

# Jobs
curl http://localhost:8000/api/v1/jobs/

# Interview
curl http://localhost:8000/api/v1/interview/history

# Footprint
curl http://localhost:8000/api/v1/footprint/history
```

---

## 🐛 Troubleshooting

### Import Errors
**Error:** `ModuleNotFoundError: No module named 'modules'`

**Solution:** Make sure you're running from the correct directory and `__init__.py` files exist.

### Circular Imports
**Error:** `ImportError: cannot import name 'X' from partially initialized module`

**Solution:** Review import order. Use `from typing import TYPE_CHECKING` for type hints.

### Router Not Found
**Error:** `AttributeError: module 'modules.auth' has no attribute 'router'`

**Solution:** Make sure each module's `__init__.py` exports the router:
```python
from .router import router
__all__ = ["router"]
```

---

## 📞 Need Help?

If you encounter issues during migration:

1. Check logs: `tail -f logs/backend.log`
2. Review architecture docs: `backend/ARCHITECTURE.md`
3. Check examples in each module
4. Reach out to the team

---

## 🎯 Success Criteria

Migration is complete when:

✅ All endpoints work with new structure  
✅ Tests pass  
✅ No import errors  
✅ Old `api/` and `models/` directories removed  
✅ Documentation updated  
✅ Team trained on new structure

---

**Good luck with the migration! 🚀**
