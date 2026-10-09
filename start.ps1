# World as a Classroom - PowerShell Launch Script
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Starting World as a Classroom (Olam Sinfxonasi)" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\python backend\run.py"

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Frontend running at: http://localhost:5173" -ForegroundColor Yellow
Write-Host "Backend running at:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Swagger API docs at: http://localhost:8000/docs" -ForegroundColor Yellow
