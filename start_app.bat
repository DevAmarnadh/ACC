@echo off
echo Starting AI Content Engine...

start "Backend API" cmd /k "python -m uvicorn api:app --reload --port 8000"
start "Frontend" cmd /k "cd frontend && npm run dev"

echo Services started!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000
