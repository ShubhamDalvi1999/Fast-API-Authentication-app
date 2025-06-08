#  Special file for Vercel serverless function

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from backend
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# Import the FastAPI app
from backend.app.api.main import app

# Export for Vercel serverless function
export_app = app 