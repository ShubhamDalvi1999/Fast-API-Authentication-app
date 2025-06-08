"""
Production Environment Runner

This script runs the FastAPI backend in production mode with PostgreSQL.
It loads environment variables from .env file and runs the server.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Ensure DATABASE_URL is available
if not os.environ.get('DATABASE_URL'):
    print("ERROR: DATABASE_URL not set in .env file!")
    print("Please copy example.env to .env and add your Neon PostgreSQL connection string.")
    sys.exit(1)

# Ensure VERCEL_ENV is set to production
if os.environ.get('VERCEL_ENV') != 'production':
    print("Setting VERCEL_ENV to production")
    os.environ['VERCEL_ENV'] = 'production'

# Check if Python dependencies are installed
try:
    import uvicorn
    from fastapi import FastAPI
    import sqlalchemy
    import python_dotenv
except ImportError:
    print("Installing required dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

print("\n" + "="*50)
print("🚀 Starting FastAPI backend in PRODUCTION mode")
print("="*50)
print("✅ Using Neon PostgreSQL database")
print(f"✅ Database URL: {os.environ.get('DATABASE_URL')[:20]}...") 
print("="*50 + "\n")

# Run FastAPI backend
if __name__ == "__main__":
    print("Starting backend server...")
    import uvicorn
    uvicorn.run("backend.app.api.main:app", host="0.0.0.0", port=8000, reload=True) 