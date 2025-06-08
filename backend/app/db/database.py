from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the absolute path to the database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = os.path.join(BASE_DIR, "database.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_URL}"

# Create a engine for the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                        connect_args={"check_same_thread": False})

# Create a session for the database which is used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the database, this is used to create the tables in the database
Base = declarative_base()