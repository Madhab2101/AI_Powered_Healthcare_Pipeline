@echo off
title 🩺 AI-Powered Predictive Healthcare Data Pipeline
chcp 65001 >nul
echo ==========================================================
echo    🚀 Starting AI-Powered Predictive Healthcare Data Pipeline
echo ==========================================================

REM ---------- 1️⃣ Activate Virtual Environment ----------
if exist "D:\BDA\AI_Powered_Healthcare_Pipeline\venv\Scripts\activate" (
    call D:\BDA\AI_Powered_Healthcare_Pipeline\venv\Scripts\activate
) else (
    echo ❌ Virtual environment not found!
    pause
    exit /b
)

REM ---------- 2️⃣ Start Kafka Server ----------
if exist "C:\tools\kafka\kafka_2.13-4.1.0\bin\windows\kafka-server-start.bat" (
    echo [1/6] Starting Kafka server...
    start "Kafka Server" cmd /k "cd /d C:\tools\kafka\kafka_2.13-4.1.0 && bin\windows\kafka-server-start.bat config\kraft\server.properties"
) else (
    echo ❌ Kafka path not found at C:\tools\kafka\kafka_2.13-4.1.0
    pause
    exit /b
)

echo.
echo 🕓 Waiting for Kafka to start on port 9092...
:WAIT_KAFKA
timeout /t 5 /nobreak >nul
netstat -ano | findstr "9092" >nul
if errorlevel 1 (
    echo ⏳ Kafka not ready yet... waiting...
    goto WAIT_KAFKA
) else (
    echo ✅ Kafka is up and running!
)

REM ---------- 3️⃣ Start Data Simulator ----------
if exist "D:\BDA\AI_Powered_Healthcare_Pipeline\data_ingestion\data_simulator.py" (
    echo [2/6] Starting Data Simulator...
    start "Data Simulator" cmd /k "cd /d D:\BDA\AI_Powered_Healthcare_Pipeline\data_ingestion && python data_simulator.py"
) else (
    echo ❌ Data simulator file not found!
)

REM ---------- 4️⃣ Start Spark Stream Processor ----------
if exist "D:\BDA\AI_Powered_Healthcare_Pipeline\spark_etl\stream_processor.py" (
    echo [3/6] Starting Spark Stream Processor...
    start "Spark Stream" cmd /k "cd /d D:\BDA\AI_Powered_Healthcare_Pipeline\spark_etl && spark-submit stream_processor.py"
) else (
    echo ❌ Spark stream script missing!
)

echo.
echo 🕓 Giving Spark 55 seconds to initialize...
timeout /t 25 /nobreak >nul

REM ---------- 5️⃣ Start FastAPI ----------
if exist "D:\BDA\AI_Powered_Healthcare_Pipeline\fastapi_server\app.py" (
    echo [4/6] Starting FastAPI server...
    start "FastAPI" cmd /k "cd /d D:\BDA\AI_Powered_Healthcare_Pipeline\fastapi_server && python app.py"
) else (
    echo ❌ FastAPI app not found!
)

echo.
echo 🕓 Waiting for FastAPI to start on port 8000...
:WAIT_FASTAPI
timeout /t 5 /nobreak >nul
netstat -ano | findstr "8000" >nul
if errorlevel 1 (
    echo ⏳ FastAPI not ready yet... waiting...
    goto WAIT_FASTAPI
) else (
    echo ✅ FastAPI server is up and running!
)

REM ---------- 6️⃣ Start Streamlit Dashboard ----------
if exist "D:\BDA\AI_Powered_Healthcare_Pipeline\streamlit_dashboard\dashboard.py" (
    echo [5/6] Starting Streamlit dashboard...
    start "Streamlit" cmd /k "cd /d D:\BDA\AI_Powered_Healthcare_Pipeline\streamlit_dashboard && streamlit run dashboard.py"
) else (
    echo ❌ Dashboard not found at streamlit_dashboard!
)

echo ==========================================================
echo ✅ All components started successfully!
echo ----------------------------------------------------------
echo 📊 Streamlit Dashboard: http://localhost:8501
echo 🌐 FastAPI API:         http://127.0.0.1:8000
echo ----------------------------------------------------------
pause
