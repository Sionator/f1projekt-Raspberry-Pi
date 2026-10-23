@echo off
cd /d "%~dp0"
echo Falls ein GitHub-Login-Fenster erscheint: bitte anmelden.
(
echo --- config ---
git config user.name "Sionator"
git config user.email "199152987+Sionator@users.noreply.github.com"
echo --- commit ---
git add .
git commit -m "Projektstart: laden.py, starten.bat, .gitignore"
git branch -M main
echo --- remote ---
git remote add origin https://github.com/Sionator/f1projekt-Raspberry-Pi.git
echo --- pull ---
git pull origin main --allow-unrelated-histories --no-edit
echo --- push ---
git push -u origin main
echo --- status ---
git status
git log --oneline
) > git_ergebnis.txt 2>&1
echo FERTIG >> git_ergebnis.txt
