@echo off
REM ============================================================
REM  MiroFish - one-click stopper
REM  Kills whatever is listening on port 5001 and 5173.
REM
REM  IMPORTANT: ASCII-only. Do not add Chinese characters.
REM ============================================================
setlocal
chcp 65001 >nul 2>&1
title MiroFish Stopper

cls
echo.
echo  ============================================================
echo                  M i r o F i s h   -   stop
echo  ============================================================
echo.

REM ---------- backend port 5001 ----------
echo  [1/2] killing port 5001 (backend) ...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5001" ^| findstr "LISTENING"') do (
    echo        kill PID %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM ---------- frontend port 5173 ----------
echo  [2/2] killing port 5173 (frontend) ...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173" ^| findstr "LISTENING"') do (
    echo        kill PID %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM ---------- Close leftover launcher windows ----------
taskkill /FI "WINDOWTITLE eq MiroFish Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq MiroFish Frontend*" /F >nul 2>&1

echo.
echo  ============================================================
echo   All MiroFish services stopped.
echo  ============================================================
echo.

timeout /t 3 /nobreak >nul
endlocal
exit /b 0
