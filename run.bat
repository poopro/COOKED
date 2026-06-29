@echo off
REM ============================================================
REM  COOKED? - repaired one-click launcher
REM  Backend (Flask, port 5001) + Frontend (Vite, port 5173)
REM
REM  ASCII-only launcher.
REM ============================================================
title COOKED? Launcher
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo  ============================================================
echo                       M i r o F i s h
echo              repaired launcher - graph and plaza
echo  ============================================================
echo  cwd: %CD%
echo.

echo  [1/5] checking project layout ...
if not exist "backend\app" goto err_layout
if not exist "frontend\package.json" goto err_layout
if not exist "frontend\node_modules\vite\bin\vite.js" goto err_frontend_deps
echo  [1/5] layout OK.

echo  [2/5] resolving Python runtime ...
set "VENV_DIR=%CD%\backend\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "CODEX_PY=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
set "PY_EXE="
set "USING_FALLBACK_PY=0"

if exist "%VENV_PY%" (
  "%VENV_PY%" -c "import sys; print(sys.executable)" >nul 2>&1
  if not errorlevel 1 set "PY_EXE=%VENV_PY%"
)

if "%PY_EXE%"=="" (
  if exist "%CODEX_PY%" (
    set "PY_EXE=%CODEX_PY%"
    set "USING_FALLBACK_PY=1"
  )
)

if "%PY_EXE%"=="" goto err_python
echo  [2/5] Python: %PY_EXE%

if "%USING_FALLBACK_PY%"=="1" (
  set "SITE_PACKAGES=%VENV_DIR%\Lib\site-packages"
  set "PYTHONPATH=%SITE_PACKAGES%;%SITE_PACKAGES%\win32;%SITE_PACKAGES%\win32\lib;%CD%\backend"
  set "PATH=%SITE_PACKAGES%\pywin32_system32;%PATH%"
)

echo  [3/5] checking backend packages ...
"%PY_EXE%" -c "import flask, dotenv, zep_cloud, httpx, openai; import pywintypes; import oasis; from camel.models import ModelFactory; print('ok')" >nul 2>&1
if errorlevel 1 goto err_backend_deps
echo  [3/5] backend packages OK.

echo  [4/5] checking .env ...
if not exist ".env" goto need_env
findstr /C:"your-openrouter-key-here" ".env" >nul 2>&1
if not errorlevel 1 goto err_placeholder_llm
findstr /C:"your-zep-key-here" ".env" >nul 2>&1
if not errorlevel 1 goto err_placeholder_zep
echo  [4/5] API keys look set.

echo  [5/5] launching backend and frontend ...
start "COOKED? Backend [5001]" cmd /k "chcp 65001 >nul && cd /d %CD%\backend && set FLASK_APP=app && set FLASK_DEBUG=True && echo === COOKED? Backend === && echo Port: 5001 && echo. && ""%PY_EXE%"" -m flask run --port 5001 --host 0.0.0.0"
start "COOKED? Frontend [5173]" cmd /k "chcp 65001 >nul && cd /d %CD%\frontend && echo === COOKED? Frontend === && echo Port: 5173 && echo. && node node_modules\vite\bin\vite.js --host 0.0.0.0 --configLoader runner"

echo  waiting ~8s for services ...
timeout /t 8 /nobreak >nul

echo.
echo  ============================================================
echo   READY
echo     Frontend : http://localhost:5173
echo     Backend  : http://localhost:5001/health
echo.
echo   To stop everything, run stop.bat
echo  ============================================================

start "" http://localhost:5173
goto end_pause

:need_env
if not exist ".env.example" goto err_no_env_example
echo  [warn] .env not found. Copying from .env.example ...
copy /Y ".env.example" ".env" >nul
echo  Please fill in your API keys, then re-run.
notepad ".env"
goto end_pause

:err_layout
echo.
echo  [FAIL] project files not found.
goto end_pause

:err_frontend_deps
echo.
echo  [FAIL] frontend dependencies are missing.
echo         Run: cd frontend && npm install
goto end_pause

:err_python
echo.
echo  [FAIL] no usable Python found.
echo         Install Python 3.12 or run this from Codex where the bundled Python exists.
goto end_pause

:err_backend_deps
echo.
echo  [FAIL] backend import check failed.
echo         The old venv packages are incomplete or incompatible.
echo         Try reinstalling: pip install flask flask-cors python-dotenv zep-cloud httpx openai pypdf camel-oasis pywin32
goto end_pause

:err_no_env_example
echo.
echo  [FAIL] neither .env nor .env.example found.
goto end_pause

:err_placeholder_llm
echo.
echo  [FAIL] LLM_API_KEY in .env is still the placeholder.
notepad ".env"
goto end_pause

:err_placeholder_zep
echo.
echo  [FAIL] ZEP_API_KEY in .env is still the placeholder.
notepad ".env"
goto end_pause

:end_pause
echo.
echo  ============================================================
echo   Press any key to close this window.
echo  ============================================================
pause >nul
exit /b 0
