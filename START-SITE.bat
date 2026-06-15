@echo off
rem Launches the Olivia Harper Homes clone at http://localhost:8765/
cd /d "%~dp0site"
start "" "http://localhost:8765/"
python -m http.server 8765
