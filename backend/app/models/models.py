from sqlalchemy import Column, Integer, String, Boolean

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True) 