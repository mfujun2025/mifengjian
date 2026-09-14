@echo off
chcp 65001 >nul
title 发布 密封件.cn 到线上
setlocal
set "PY=C:\Users\Huawei\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

cd /d "%~dp0"

echo ========================================================
echo  发布 密封件.cn 到线上
echo ========================================================
echo.
echo [1/2] 重新构建站点...
"%PY%" build.py
if errorlevel 1 (
  echo.
  echo [!] 构建失败，已中止发布。请检查上面的错误信息。
  echo.
  pause
  exit /b 1
)
echo.
echo [2/2] 上传到 GitHub...
"%PY%" deploy.py
if errorlevel 1 (
  echo.
  echo [!] 发布失败，已中止。请检查上面的错误信息。
  echo.
  pause
  exit /b 1
)
echo.
pause
