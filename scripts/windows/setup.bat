@echo off

@REM Install Python using WinGet if necessary
python --version >nul 2>&1 || ( winget install -e --id Python.Python.3.10 )

@REM Install ffmpeg using WinGet if necessary
ffmpeg -version >nul 2>&1 || ( winget install ffmpeg )

@REM Refresh the environment vars so any installed commands above are active
call refresh_env.bat

@REM Set up the venv if it needs to be
if not exist ..\..\.venv\ ( python -m venv ..\..\.venv )

@REM Install required scripts
..\..\.venv\Scripts\pip.exe install -r ..\..\requirements.txt

@REM Activate the new venv
..\..\.venv\Scripts\activate.bat
