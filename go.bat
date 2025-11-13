@echo on
REM --- Conda Activation ---
call "C:\Users\affan\anaconda3\condabin\conda.bat" activate space

if errorlevel 1 (
    echo ERROR: Conda activation failed.
    pause
    exit /b 1
)

REM --- Script Execution ---
REM FIX: Use /D to change drive (C: to D:) AND directory
cd /D "D:\Data Project\Launching Rocket\rocket-launch"

if errorlevel 1 (
    echo ERROR: Could not find project directory. Check the path.
    pause
    exit /b 1
)

REM Running the correct file name (LL2_API.py based on your error)
python LL2_API.py

echo.
echo Data collection attempt finished.
timeout 5