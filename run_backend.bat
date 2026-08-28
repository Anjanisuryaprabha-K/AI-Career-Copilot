@echo off
set USE_IN_MEMORY_DB=false
set PYTHONPATH=%~dp0backend
cd /d %~dp0backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
