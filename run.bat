@echo off
REM ============================================================
REM  MiroFish - one-click launcher
REM  Backend (Flask, port 5001) + Frontend (Vite, port 5173)
REM  Just double-click this file.
REM
REM  IMPORTANT: ASCII-only.  Do not add Chinese characters.
REM  This script always pauses at the end so you can read errors.
REM ============================================================
title MiroFish Launcher
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo  ============================================================
echo                       M i r o F i s h
echo               Founder Sandbox  -  one-click start
echo  ============================================================
echo  cwd: %CD%
echo.

REM ---------- step 1: project layout ----------
echo  [1/5] checking project layout ...
if not exist "backend\app" goto err_layout
if not exist "frontend\package.json" goto err_layout
if not exist "backend\.venv\Scripts\python.exe" goto err_venv
echo  [1/5] layout OK.

REM ---------- step 2: backend deps ----------
if exist "backend\.venv\.mirofish_deps_ok" goto skip_dep_check
echo  [2/5] checking backend python packages ...
echo        (first run can take ~30s, please wait)
"backend\.venv\Scripts\python.exe" -c "import flask, dotenv, zep_cloud, httpx; from camel.models import ModelFactory; import oasis" 2>nul
if errorlevel 1 goto install_deps
echo  [2/5] backend packages OK.
echo ok > "backend\.venv\.mirofish_deps_ok"
goto step3

:install_deps
echo  [2/5] some packages missing, auto-installing (this may take 5-10 min, downloading torch + transformers) ...
"backend\.venv\Scripts\python.exe" -m ensurepip --upgrade >nul 2>&1
"backend\.venv\Scripts\python.exe" -m pip install --upgrade pip >nul 2>&1
"backend\.venv\Scripts\python.exe" -m pip install --ignore-requires-python flask flask-cors python-dotenv zep-cloud httpx pypdf camel-oasis
if errorlevel 1 goto err_pip
REM verify install actually worked
"backend\.venv\Scripts\python.exe" -c "import flask, dotenv, zep_cloud, httpx; from camel.models import ModelFactory; import oasis" 2>nul
if errorlevel 1 goto err_pip
echo  [2/5] packages installed.
echo ok > "backend\.venv\.mirofish_deps_ok"
goto step3

:skip_dep_check
echo  [2/5] backend packages OK (cached).

:step3
REM ---------- step 3: .env exists ----------
echo  [3/5] checking .env ...
if not exist ".env" goto need_env
echo  [3/5] .env exists.
goto step4

:need_env
if not exist ".env.example" goto err_no_env_example
echo  [warn] .env not found.  Copying from .env.example ...
copy /Y ".env.example" ".env" >nul
echo  Please open .env and fill in your API keys, then re-run.
notepad ".env"
goto end_pause

:step4
REM ---------- step 4: API keys placeholder check ----------
echo  [4/5] checking API keys ...
findstr /C:"your-openrouter-key-here" ".env" >nul 2>&1
if not errorlevel 1 goto err_placeholder_llm
findstr /C:"your-zep-key-here" ".env" >nul 2>&1
if not errorlevel 1 goto err_placeholder_zep
echo  [4/5] API keys look set.

REM ---------- step 5: launch ----------
echo  [5/5] launching backend and frontend ...
start "MiroFish Backend [5001]" cmd /k "chcp 65001 >nul && cd /d %~dp0backend && set FLASK_APP=app && set FLASK_DEBUG=True && echo === MiroFish Backend === && echo Port: 5001 && echo. && .venv\Scripts\python.exe -m flask run --port 5001 --host 0.0.0.0"
start "MiroFish Frontend [5173]" cmd /k "chcp 65001 >nul && cd /d %~dp0frontend && echo === MiroFish Frontend === && echo Port: 5173 && echo. && npm run dev"

echo  waiting ~10s for services ...
timeout /t 10 /nobreak >nul

echo.
echo  ============================================================
echo   READY
echo     Frontend : http://localhost:5173
echo     Backend  : http://localhost:5001/health
echo.
echo   To stop everything, run stop.bat
echo  ============================================================

start "" http://localhost:5173

echo.
echo  Backend / frontend keep running in their own windows.
goto end_pause


REM ============================================================
REM  Error handlers (each one prints message and falls through to pause)
REM ============================================================
:err_layout
echo.
echo  [FAIL] project files not found.
echo         Make sure run.bat lives in the MiroFish project root,
echo         next to backend\ and frontend\ folders.
goto end_pause

:err_venv
echo.
echo  [FAIL] backend\.venv not found.
echo         First-time setup:
echo           cd backend
echo           python -m venv .venv
echo           .venv\Scripts\activate
echo           pip install -r requirements.txt
goto end_pause

:err_pip
echo.
echo  [FAIL] pip install / import verify failed.  Run manually:
echo           cd backend
echo           .venv\Scripts\activate
echo           pip install --ignore-requires-python flask flask-cors python-dotenv zep-cloud httpx pypdf camel-oasis
echo  Removing stale dep cache so next run rechecks ...
del /F /Q "backend\.venv\.mirofish_deps_ok" >nul 2>&1
goto end_pause

:err_no_env_example
echo.
echo  [FAIL] neither .env nor .env.example found.
goto end_pause

:err_placeholder_llm
echo.
echo  [FAIL] LLM_API_KEY in .env is still the placeholder.
echo         Open .env, paste your real OpenRouter key, then re-run.
notepad ".env"
goto end_pause

:err_placeholder_zep
echo.
echo  [FAIL] ZEP_API_KEY in .env is still the placeholder.
echo         Open .env, paste your real Zep key, then re-run.
notepad ".env"
goto end_pause


:end_pause
echo.
echo  ============================================================
echo   Press any key to close this window.
echo  ============================================================
pause >nul
exit /b 0
