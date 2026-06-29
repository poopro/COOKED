@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === COOKED? Backend ===
echo Port: 5001
echo.
set "PY_EXE=%~dp0.venv\Scripts\python.exe"
set "FLASK_APP=app"
set "FLASK_DEBUG=True"
"%PY_EXE%" -m flask run --port 5001 --host 0.0.0.0 --no-reload
