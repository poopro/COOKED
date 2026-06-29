@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === COOKED? Frontend ===
echo Port: 5173
echo.
node node_modules\vite\bin\vite.js --host 0.0.0.0 --configLoader runner