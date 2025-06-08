# Deploying to Vercel

This document explains how to deploy this fullstack application (React frontend + FastAPI backend) to Vercel.

## Project Structure

The project has two main components:
- `frontend/`: Contains the React application
- `backend/`: Contains the FastAPI backend

## Deployment Configuration

The deployment is configured via the `vercel.json` file in the root directory. This file tells Vercel how to build and route requests to both the frontend and backend.

## How It Works

1. **Building the Application**:
   - The frontend React app is built using the Vercel static build process
   - The FastAPI backend is deployed as a Python serverless function

2. **Routing**:
   - API requests (`/api/*` and `/auth/*`) are routed to the FastAPI backend
   - All other requests are served from the React frontend

## Deployment Steps

1. **Prerequisites**:
   - A GitHub repository containing your code
   - A Vercel account

2. **Deploy to Vercel**:
   - Log in to Vercel and click "New Project"
   - Import your GitHub repository
   - Configure the project settings (no special settings required as everything is in `vercel.json`)
   - Click "Deploy"

3. **Environment Variables**:
   - Add any necessary environment variables in the Vercel project settings
   - For database connections, consider using a managed database service like Supabase or Planetscale

## Local Development

For local development, continue using:
- `cd frontend && npm start` for the React frontend
- `cd backend && python main.py` for the FastAPI backend

## Troubleshooting

If you encounter deployment issues:
1. Check the Vercel build logs for errors
2. Ensure all dependencies are properly listed in `requirements.txt`
3. Verify the paths in `vercel.json` match your project structure 