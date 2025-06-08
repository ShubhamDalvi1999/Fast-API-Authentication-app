# FastAPI Authentication App with React Frontend

A simple authentication application with FastAPI backend and React frontend.

## Features

- User registration and login
- JWT-based authentication
- Protected routes
- Simple React UI

## Project Structure

- `backend/`: FastAPI backend
  - `app/`: Application package
    - `api/`: API endpoints
    - `core/`: Core functionality (auth, security)
    - `db/`: Database setup
    - `models/`: Database models
  - `main.py`: Entry point
- `frontend/`: React frontend

## Setup and Running

### Backend (FastAPI)

1. Navigate to the backend directory:
```
cd backend
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the server:
```
python main.py
```

The backend will run on http://localhost:8000

### Frontend (React)

1. Navigate to the frontend directory:
```
cd frontend
```

2. Install dependencies:
```
npm install
```

3. Start the development server:
```
npm start
```

The frontend will run on http://localhost:3000

## API Endpoints

- `POST /auth/`: Register a new user
- `POST /auth/token`: Login and get access token
- `GET /auth/users/me`: Get current user information (protected)
- `GET /`: Root endpoint (protected)

## Authentication Flow

1. Register a user with username and password
2. Login to obtain a JWT token
3. Include the token in the Authorization header for protected endpoints
4. Token expires after 20 minutes

## Deployment on Vercel

This application is configured for easy deployment on Vercel.

### Steps to Deploy

1. Push your code to GitHub
2. Import your repository in Vercel
3. Vercel will automatically detect the configuration and deploy both frontend and backend

### Configuration Files

- `vercel.json`: Main configuration for Vercel deployment
- `api/index.py`: Serverless function entry point for the backend
- `requirements.txt`: Python dependencies for the backend

### Environment Variables

You may need to set these environment variables in Vercel:

- `SECRET_KEY`: Your application's secret key (same as in auth.py)

### Checking Deployment

After deployment, your application will be available at:
- Frontend: `https://your-project-name.vercel.app/`
- Backend API: `https://your-project-name.vercel.app/api/`
- Auth endpoints: `https://your-project-name.vercel.app/auth/`

## Tech Stack

- Backend: FastAPI, SQLAlchemy, JWT
- Frontend: React, React Router, Axios 