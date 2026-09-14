@echo off
chcp 65001 >nul
title Seal-cn  form setup
setlocal
set "PY=C:\Users\Huawei\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" "%~dp0setup_form.py"
if errorlevel 1 (
  echo.
  echo [!] Script exited with an error. Check the messages above.
)
echo.
pause
