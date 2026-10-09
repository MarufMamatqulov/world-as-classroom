@echo off
echo ========================================================
echo  Starting World as a Classroom (Olam Sinfxonasi)
echo ========================================================

echo [1/2] Starting FastAPI Backend on http://localhost:8000...
start "World Classroom - Backend" cmd /k ".\venv\Scripts\python backend\run.py"

echo [2/2] Starting Vite Frontend on http://localhost:5173...
start "World Classroom - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are launching!
echo Frontend: http://localhost:5173
echo Backend API Docs: http://localhost:8000/docs
echo ========================================================
pause
