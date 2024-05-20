@echo off
setlocal

:: Change directory to the location of the batch file
cd /d "%~dp0"

:: Check if the executable exists
if not exist "dist\MyDjangoApp\MyDjangoApp.exe" (
    echo Executable not found, please verify the path.
    pause
    exit /b 1
)

:: Start the server and redirect output to server_output.txt
echo Executable found, starting server...
start "" /b "dist\MyDjangoApp.exe" > "dist\MyDjangoApp\server_output.txt" 2>&1

:: Wait for a short period to give the server time to start
timeout /t 5 /nobreak >nul

:: Check if the server is running by looking for the output file
findstr /c:"Starting development server" "dist\MyDjangoApp\server_output.txt" >nul
if errorlevel 1 (
    echo Server did not start correctly. Check server_output.txt for errors.
    type "dist\MyDjangoApp\server_output.txt"
    pause
    exit /b 1
)

:: Open the default web browser
start http://127.0.0.1:8000/

pause
exit /b 0
