@echo off
title 🛑 AI-Powered Predictive Healthcare Data Pipeline
chcp 65001 >nul
echo ==========================================================
echo    🧹 AI-Powered Predictive Healthcare Data Pipeline
echo ==========================================================

REM ---------- 1️⃣ Stop Streamlit ----------
echo [1/5] Stopping Streamlit Dashboard...
taskkill /F /IM "streamlit.exe" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Streamlit*" >nul 2>&1

REM ---------- 2️⃣ Stop FastAPI ----------
echo [2/5] Stopping FastAPI Server...
taskkill /F /FI "WINDOWTITLE eq FastAPI*" >nul 2>&1
taskkill /F /IM "python.exe" /FI "WINDOWTITLE eq FastAPI*" >nul 2>&1

REM ---------- 3️⃣ Stop Spark ----------
echo [3/5] Stopping Spark Stream Processor...
taskkill /F /FI "WINDOWTITLE eq Spark Stream*" >nul 2>&1
taskkill /F /IM "java.exe" /FI "WINDOWTITLE eq Spark*" >nul 2>&1

REM ---------- 4️⃣ Stop Kafka ----------
echo [4/5] Stopping Kafka Server...
taskkill /F /FI "WINDOWTITLE eq Kafka Server*" >nul 2>&1
taskkill /F /IM "java.exe" /FI "WINDOWTITLE eq Kafka*" >nul 2>&1

REM ---------- 5️⃣ Stop Data Simulator ----------
echo [5/5] Stopping Data Simulator...
taskkill /F /FI "WINDOWTITLE eq Data Simulator*" >nul 2>&1
taskkill /F /IM "python.exe" /FI "WINDOWTITLE eq Data Simulator*" >nul 2>&1

REM ---------- Cleanup residual python/java ----------
echo.
echo 🧽 Cleaning up background processes...
taskkill /F /IM "python.exe" >nul 2>&1
taskkill /F /IM "java.exe" >nul 2>&1

echo.
echo ==========================================================
echo ✅ All pipeline processes have been stopped successfully!
echo ----------------------------------------------------------
pause
