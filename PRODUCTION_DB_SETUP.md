# Production Database Setup Guide

## Issue
The database schema was not being created in production (Neon PostgreSQL) because the code was preventing table creation when `VERCEL_ENV=production`.

## Solutions Implemented

### 1. ✅ **Automatic Table Creation (Fixed)**
- **File**: `backend/app/api/main.py`
- **Change**: Removed the condition that prevented table creation in production
- **Result**: Tables will now be created automatically on first deployment

### 2. 🔧 **Manual Initialization Endpoint**
- **Endpoint**: `POST /api/init-db`
- **Method**: Send a POST request with the correct `init_key`
- **Key**: Set via environment variable `INIT_DB_KEY`

### 3. 📊 **Database Status Check**
- **Endpoint**: `GET /api/db-status`
- **Purpose**: Check if tables exist and count users
- **Usage**: Visit your deployed app URL + `/api/db-status`

### 4. 🖥️ **Local Initialization Script**
- **File**: `backend/init_production_db.py`
- **Usage**: Run locally with production environment variables

## How to Verify the Fix

### Step 1: Check Database Status
Visit your deployed app and check:
```
https://your-app.vercel.app/api/db-status
```

Expected response:
```json
{
  "status": "ok",
  "database_connected": true,
  "all_tables": ["users"],
  "users_table": {
    "exists": true,
    "columns": ["id", "username", "hashed_password", "is_active"]
  },
  "user_count": 0,
  "environment": "production"
}
```

### Step 2: Test User Registration
Try registering a user via the frontend or API:
```bash
curl -X POST "https://your-app.vercel.app/api/auth/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Step 3: Manual Initialization (if needed)
If tables still don't exist, use the manual endpoint:
```bash
curl -X POST "https://your-app.vercel.app/api/init-db" \
  -d "init_key=YOUR_INIT_DB_KEY"
```

## Environment Variables Required

### Vercel Environment Variables
1. **DATABASE_URL**: Your Neon PostgreSQL connection string
   ```
   postgresql://username:password@host:port/database
   ```

2. **INIT_DB_KEY**: (Optional) Secret key for manual initialization
   ```
   your-secret-initialization-key
   ```

3. **SECRET_KEY**: (Existing) JWT secret key
   ```
   your-jwt-secret-key
   ```

## Troubleshooting

### Issue: Tables not created on deployment
**Solution**: The fix should resolve this automatically. If not, use the manual init endpoint.

### Issue: Connection errors
**Check**: 
1. DATABASE_URL is correctly set in Vercel
2. Neon database is running and accessible
3. Connection string format is correct

### Issue: Permission errors
**Check**: Neon database user has CREATE TABLE permissions

## Expected Database Schema

After successful initialization, your Neon database should have:

**Table: `users`**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    hashed_password VARCHAR(100),
    is_active BOOLEAN DEFAULT true
);
```

## Next Steps

1. **Deploy** the updated code to Vercel
2. **Check** `/api/db-status` to verify schema creation
3. **Test** user registration and login
4. **Monitor** your Neon dashboard for data 