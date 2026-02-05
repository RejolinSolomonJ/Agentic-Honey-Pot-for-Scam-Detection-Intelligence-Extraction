@echo off
start /min python run_forever.py
echo Server is running in the background!
echo Check connection_info.txt for your proper URL.
echo.
echo To stop it, run: taskkill /F /IM python.exe /IM pythonw.exe
pause
