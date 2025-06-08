from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
import sys
import os

# Add the parent directory to sys.path for local development
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    print(f"Added {parent_dir} to sys.path from models.py")

# Fix imports for different environments
try:
    # Try relative imports first
    from ..db.database import Base
    print("Models: Using relative imports")
except ImportError:
    try:
        # Try absolute imports with backend prefix
        from backend.app.db.database import Base
        print("Models: Using backend.app.* imports")
    except ImportError:
        # Fallback to local imports
        from app.db.database import Base
        print("Models: Using app.* imports")

class User(Base):
    __tablename__ = "users"
    # Add extend_existing to avoid errors when model is imported multiple times
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True) 