from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from typing import Annotated, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.db.database import Base, engine, SessionLocal
from app.models.models import User
from app.core import auth
from app.core.auth import get_current_user
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app", "*"],  # Allow Vercel domains and local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

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


## running the app using uvicorn : uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 