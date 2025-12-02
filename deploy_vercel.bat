@echo off
echo ========================================
echo  Vercel Frontend Deployment Script
echo ========================================
echo.

cd frontend

echo [Step 1] Installing dependencies...
call npm install

echo.
echo [Step 2] Building for production...
call npm run build

echo.
echo [Step 3] Deploying to Vercel...
echo.
echo NOTE: Make sure you've updated the backend URL in the Vercel dashboard!
echo Environment Variable: VITE_API_URL = https://your-backend.onrender.com/api/v1
echo.

call vercel --prod

echo.
echo ========================================
echo  Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy the Vercel URL from above
echo 2. Go to Render dashboard
echo 3. Update CORS_ORIGINS environment variable
echo 4. Add your Vercel URL to the allowed origins
echo.
pause

