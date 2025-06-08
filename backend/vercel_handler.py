from app.api.main import app
import os

# This is necessary for Vercel serverless functions
# It exposes the ASGI application for Vercel's Python runtime

# The handler will be imported by Vercel
handler = app 