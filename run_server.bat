@echo off
echo Starting Agentic Honey-Pot Server...
echo API Documentation: http://localhost:8000/docs
echo.
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
