@echo off
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Running verification script...
python test_fallback.py
pause
