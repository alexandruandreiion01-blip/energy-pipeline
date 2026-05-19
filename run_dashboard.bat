@echo off
cd /d "%~dp0"
set PATH=%PATH%;C:\Program Files\PostgreSQL\18\bin
streamlit run dashboard.py
pause