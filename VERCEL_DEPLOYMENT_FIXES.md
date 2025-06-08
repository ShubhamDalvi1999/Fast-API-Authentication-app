# Vercel Deployment Fixes

## Issues Fixed

### 1. Wrong Function Entry Point
- **Problem**: `vercel.json` was pointing to `backend/app/api/main.py`, but Vercel expects serverless functions in the root `api/` directory.
- **Solution**: Created `api/main.py` that imports and wraps the FastAPI app from the backend.

### 2. Simplified Routing Configuration
- **Problem**: Complex routing rules with multiple specific endpoints that were causing 404s.
- **Solution**: Simplified to two main routes:
  - `/api/*` → `api/main.py` (for all API endpoints)
  - `/*` → `frontend/$1` (for static files)

### 3. Proper Static File Handling
- **Problem**: Frontend static files weren't being served correctly.
- **Solution**: Added proper static build configuration with `@vercel/static-build` and `distDir: "build"`.

## File Changes

### New Files
- `api/main.py` - Vercel serverless function entry point

### Modified Files
- `vercel.json` - Simplified configuration with proper routing

## Configuration Details

### vercel.json Structure
```json
{
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json", 
      "use": "@vercel/static-build",
      "config": { "distDir": "build" }
    }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/main.py" },
    { "src": "/(.*)", "dest": "/frontend/$1" }
  ]
}
```

### Environment Variables
- `PYTHONPATH=.` - Ensures root directory is in Python path
- `VERCEL_ENV=production` - Identifies production environment

## Testing

After deployment, test these endpoints:
- `/api/health-check` - Basic health check
- `/api/debug` - Environment debug information
- `/api/db-test` - Database connectivity test

## Notes

- The FastAPI app maintains its original import structure with fallback logic
- All existing endpoints should work without changes
- Frontend build process remains the same
- Database initialization still requires calling `/api/init-db` with proper key 