# Backend Architecture - Domain-Driven Design

> **Modern, scalable backend architecture organized by domain/feature modules**

## 🏗️ Architecture Overview

This backend follows **Domain-Driven Design (DDD)** principles, organizing code by **business domains** (features) rather than technical layers. This approach provides:

- ✅ **Better Scalability** - Easy to add new features
- ✅ **Clear Boundaries** - Each module is self-contained
- ✅ **Team Collaboration** - Teams can work on different modules independently
- ✅ **Easier Testing** - Test each domain in isolation
- ✅ **Reduced Coupling** - Modules are loosely coupled

---

## 📁 Directory Structure

```
backend/app/
├── modules/                          # Feature-based organization
│   ├── auth/                         # Authentication & Authorization
│   │   ├── __init__.py
│   │   ├── router.py                 # FastAPI routes (/api/auth/*)
│   │   ├── schemas.py                # Pydantic models (request/response)
│   │   ├── service.py                # Business logic
│   │   ├── models.py                 # Database models (User)
│   │   └── dependencies.py           # Route dependencies
│   │
│   ├── resume/                       # Resume Analysis & Enhancement
│   │   ├── __init__.py
│   │   ├── router.py                 # FastAPI routes (/api/resume/*)
│   │   ├── schemas.py                # Request/response models
│   │   ├── service.py                # Resume processing logic
│   │   ├── models.py                 # Database models (Resume)
│   │   └── utils.py                  # Resume-specific utilities
│   │
│   ├── jobs/                         # Job Matching & Recommendations
│   │   ├── __init__.py
│   │   ├── router.py                 # FastAPI routes (/api/jobs/*)
│   │   ├── schemas.py                # Request/response models
│   │   ├── service.py                # Job service logic
│   │   ├── models.py                 # Database models (Job)
│   │   └── matcher.py                # Job matching algorithm
│   │
│   ├── interview/                    # AI Interview Simulator
│   │   ├── __init__.py
│   │   ├── router.py                 # FastAPI routes (/api/interview/*)
│   │   ├── schemas.py                # Request/response models
│   │   ├── service.py                # Interview service logic
│   │   ├── models.py                 # Database models (Interview)
│   │   └── simulator.py              # Interview simulation logic
│   │
│   └── footprint/                    # Digital Footprint Scanner
│       ├── __init__.py
│       ├── router.py                 # FastAPI routes (/api/footprint/*)
│       ├── schemas.py                # Request/response models
│       ├── service.py                # Footprint service logic
│       ├── models.py                 # Database models (Footprint)
│       └── scanners.py               # GitHub/StackOverflow scanners
│
├── shared/                           # Shared across modules
│   ├── __init__.py
│   ├── database.py                   # Database session management
│   ├── security.py                   # JWT, password hashing
│   ├── dependencies.py               # Common dependencies
│   ├── middleware.py                 # CORS, rate limiting
│   ├── exceptions.py                 # Base exceptions
│   └── validators.py                 # Input validators
│
├── core/                             # Core configuration
│   ├── __init__.py
│   ├── config.py                     # Settings & configuration
│   └── events.py                     # Startup/shutdown events
│
└── main.py                           # FastAPI app initialization
```

---

## 🎯 Module Structure Pattern

Each module follows a consistent structure:

### `router.py`
- FastAPI routes (endpoints)
- Request/response handling
- OpenAPI documentation
- Example:
  ```python
  from fastapi import APIRouter, Depends
  from .schemas import UserCreate, UserResponse
  from .service import AuthService
  
  router = APIRouter(prefix="/api/auth", tags=["Authentication"])
  
  @router.post("/register", response_model=UserResponse)
  async def register(user: UserCreate, service: AuthService = Depends()):
      return await service.register(user)
  ```

### `schemas.py`
- Pydantic models for validation
- Request/response data structures
- Example:
  ```python
  from pydantic import BaseModel, EmailStr
  
  class UserCreate(BaseModel):
      email: EmailStr
      password: str
  
  class UserResponse(BaseModel):
      id: int
      email: str
      created_at: datetime
  ```

### `service.py`
- Business logic
- Orchestrates between router and models
- Example:
  ```python
  class AuthService:
      async def register(self, user: UserCreate) -> UserResponse:
          # Hash password, create user, send email, etc.
          pass
  ```

### `models.py`
- Database models (SQLAlchemy, etc.)
- Database operations
- Example:
  ```python
  from sqlalchemy import Column, Integer, String
  
  class User:
      id = Column(Integer, primary_key=True)
      email = Column(String, unique=True)
      hashed_password = Column(String)
  ```

### `dependencies.py` (optional)
- Module-specific dependencies
- Permission checks
- Example:
  ```python
  from fastapi import Depends, HTTPException
  
  async def get_current_user(token: str = Depends(oauth2_scheme)):
      # Validate token and return user
      pass
  ```

---

## 🔗 Module Communication

### ✅ Good Practices:

1. **Through Service Layer:**
   ```python
   # In modules/resume/service.py
   from modules.auth.service import AuthService
   
   class ResumeService:
       def __init__(self, auth_service: AuthService):
           self.auth_service = auth_service
   ```

2. **Through Shared Dependencies:**
   ```python
   # In modules/resume/router.py
   from shared.dependencies import get_current_user
   
   @router.post("/upload")
   async def upload(user = Depends(get_current_user)):
       pass
   ```

### ❌ Avoid:

1. **Direct Model Imports Across Modules:**
   ```python
   # DON'T DO THIS
   from modules.auth.models import User  # ❌ Creates tight coupling
   ```

2. **Router-to-Router Communication:**
   ```python
   # DON'T DO THIS
   from modules.auth.router import some_function  # ❌ Wrong layer
   ```

---

## 🚀 Adding a New Module

### Step 1: Create Module Directory
```bash
mkdir -p backend/app/modules/new_module
cd backend/app/modules/new_module
```

### Step 2: Create Module Files
```bash
touch __init__.py router.py schemas.py service.py models.py
```

### Step 3: Implement Router
```python
# router.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/new-module", tags=["New Module"])

@router.get("/")
async def list_items():
    return {"items": []}
```

### Step 4: Register in Main App
```python
# backend/app/main.py
from modules.new_module.router import router as new_module_router

app.include_router(new_module_router)
```

---

## 🧪 Testing Strategy

### Module Testing (Unit Tests)
```python
# tests/modules/test_auth_service.py
from modules.auth.service import AuthService

def test_register():
    service = AuthService()
    result = service.register(UserCreate(...))
    assert result.email == "test@example.com"
```

### Integration Testing
```python
# tests/integration/test_auth_flow.py
from fastapi.testclient import TestClient

def test_registration_flow(client: TestClient):
    response = client.post("/api/auth/register", json={...})
    assert response.status_code == 201
```

---

## 📊 Benefits Over Layer-Based Architecture

### Old Structure (Technical Layers):
```
backend/app/
├── api/          # All routes mixed together
├── models/       # All models mixed together
└── core/         # All logic mixed together
```
**Problems:**
- ❌ Hard to find related code
- ❌ Difficult to understand feature scope
- ❌ Changes affect multiple layers
- ❌ Poor team collaboration

### New Structure (Domain Modules):
```
backend/app/
├── modules/
│   ├── auth/     # Everything auth-related
│   ├── resume/   # Everything resume-related
│   └── jobs/     # Everything jobs-related
```
**Benefits:**
- ✅ All feature code in one place
- ✅ Clear feature boundaries
- ✅ Easy to add/remove features
- ✅ Better team ownership

---

## 🔧 Migration Path

### Phase 1: Parallel Structure (Current)
- ✅ New structure created
- ⚠️ Old structure still exists
- 🔄 Gradually move logic to new structure

### Phase 2: Update Imports
- Update `main.py` to use new routers
- Update tests to use new paths
- Update documentation

### Phase 3: Remove Old Structure
- Delete `api/` directory
- Delete `models/` directory  
- Keep only `modules/`, `shared/`, `core/`

---

## 📚 Related Patterns

- **Clean Architecture** - Separation of concerns
- **Hexagonal Architecture** - Ports and adapters
- **CQRS** - Command Query Responsibility Segregation
- **Repository Pattern** - Data access abstraction

---

## 🎓 Learning Resources

- [Domain-Driven Design by Eric Evans](https://www.domainlanguage.com/ddd/)
- [Clean Architecture by Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)

---

## 👥 Team Guidelines

1. **One Feature = One Module** - If it's a distinct feature, it gets its own module
2. **Keep Modules Independent** - Minimize cross-module dependencies
3. **Shared Code Goes in `shared/`** - Don't duplicate across modules
4. **Document Module Purpose** - Add README in each module directory
5. **Review Module Boundaries** - Refactor if modules become too large

---

**Made with ❤️ for scalable backend architecture**
