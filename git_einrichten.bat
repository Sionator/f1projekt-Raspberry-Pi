@echo off
cd /d "%~dp0"
(
echo --- Version ---
git --version
echo --- Name / E-Mail ---
git config user.name
git config user.email
echo --- init ---
git init
echo --- add ---
git add .
echo --- commit ---
git commit -m "Start"
git branch -M main
echo --- status ---
git status
git log --oneline
) > git_ergebnis.txt 2>&1
