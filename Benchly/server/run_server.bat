@echo off
REM Run Benchly server (Windows batch)
SET PORT=%PORT%
IF "%PORT%"=="" SET PORT=5000
IF "%BENCHLY_DB_PATH%"=="" SET BENCHLY_DB_PATH=%~dp0benchly.db
python -m server.app
