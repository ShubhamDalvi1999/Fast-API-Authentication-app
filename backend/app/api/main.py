from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from typing import Annotated, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import sys, os
# Fix imports for Vercel deployment
try:
    from backend.app.db.database import Base, engine, SessionLocal
    from backend.app.models.models import User
    from backend.app.core import auth
    from backend.app.core.auth import get_current_user
except ImportError:
    # Fallback to local imports
    from app.db.database import Base, engine, SessionLocal
    from app.models.models import User
    from app.core import auth
    from app.core.auth import get_current_user
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import traceback


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app", "*"],  # Allow Vercel domains and local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
try:
    app.include_router(auth.router)
except Exception as e:
    print(f"Error including router: {str(e)}")

# Create database tables if not in production
if os.environ.get("VERCEL_ENV") != "production":
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency,  db : db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return {"User": user}


# For Vercel serverless function
@app.get("/api/health-check")
async def health_check():
    return {"status": "ok", "message": "FastAPI backend is running!"}


# Simple health check for troubleshooting
@app.get("/health")
async def basic_health():
    return {"status": "ok"}


# Detailed environment check
@app.get("/api/debug")
async def debug_info():
    try:
        # Get environment info
        env_info = {
            "VERCEL_ENV": os.environ.get("VERCEL_ENV"),
            "PYTHONPATH": os.environ.get("PYTHONPATH"),
            "DATABASE_URL": os.environ.get("DATABASE_URL", "Not set").replace(
                os.environ.get("PGPASSWORD", ""), "[REDACTED]"
            ) if os.environ.get("DATABASE_URL") else "Not set",
            "sys.path": sys.path,
            "current_directory": os.getcwd(),
            "directory_contents": os.listdir(".")
        }
        
        # Test database connection without exposing credentials
        db_status = "Not tested"
        try:
            db = SessionLocal()
            result = db.execute("SELECT 1").scalar()
            db.close()
            db_status = f"Connected successfully (test query result: {result})"
        except Exception as e:
            db_status = f"Connection failed: {str(e)}"
            
        return {
            "status": "ok",
            "environment": env_info,
            "database": db_status
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }


# Database connection test
@app.get("/api/db-test")
async def test_db_connection():
    try:
        # Test creating a session
        db = SessionLocal()
        # Run a simple query
        result = db.execute("SELECT 1").scalar()
        db.close()
        return {"status": "ok", "connected": True, "test_query": result}
    except Exception as e:
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}


## running the app using uvicorn : uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 