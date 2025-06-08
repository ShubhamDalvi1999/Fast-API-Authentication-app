from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Check if we're in development or production mode
IS_PRODUCTION = os.environ.get("VERCEL_ENV") == "production"

if IS_PRODUCTION:
    # Use Neon PostgreSQL in production
    DATABASE_URL = os.environ.get("DATABASE_URL")
    
    # For SQLAlchemy 1.4+ compatibility
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Create engine for PostgreSQL
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Helps with connection issues after idle time
        pool_recycle=300,    # Recycle connections every 5 minutes
        pool_size=20,        # Maximum number of connections in pool
        max_overflow=10      # Maximum number of connections that can be created beyond pool_size
    )
else:
    # Use SQLite in development
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_URL = os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_URL}"
    
    # Create engine for SQLite
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# Create a session for the database which is used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the database, this is used to create the tables in the database
Base = declarative_base()