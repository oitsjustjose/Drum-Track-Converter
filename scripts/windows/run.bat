@REM @echo off

call setup.bat

cd ..\..

start /B cmd /C call .venv\Scripts\python.exe -m src.gui

cd scripts\windows