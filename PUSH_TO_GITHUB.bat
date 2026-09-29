@echo off
title Publish to GitHub
cd /d "%~dp0"
echo ===================================================
echo   Publishing to GitHub (Vivek0510Yadav)
echo ===================================================
echo.
git remote remove origin 2>nul
git remote add origin https://github.com/Vivek0510Yadav/telegram-lecture-downloader.git
git branch -M main
echo Pushing branch 'main' to GitHub...
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ===================================================
    echo   SUCCESS! Your project is published on GitHub:
    echo   https://github.com/Vivek0510Yadav/telegram-lecture-downloader
    echo ===================================================
) else (
    echo.
    echo If the push failed with 404 / Not Found, make sure
    echo you created the repository 'telegram-lecture-downloader'
    echo on https://github.com/new first!
)
pause
