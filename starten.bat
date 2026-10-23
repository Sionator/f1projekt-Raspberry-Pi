@echo off
cd /d "%~dp0"
if not exist cache mkdir cache
call venv\Scripts\activate.bat
echo Lade Rennen... bitte warten
python laden.py > ergebnis.txt 2>&1
echo FERTIG >> ergebnis.txt
