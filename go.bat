@echo on
REM --- Conda Activation ---
REM 1. Call the official Conda initialization script and activate the 'space' environment.
REM    NOTE: Verify 'C:\Users\affan\Miniconda3' is the correct installation folder for you.
call "C:\Users\affan\anaconda3\condabin\conda.bat" activate space

REM Check if activation failed
if errorlevel 1 (
    echo.
    echo ERROR: Conda environment 'space' failed to activate. Check the path above.
    pause
    exit /b 1
)

REM --- Script Execution ---
REM 2. Navigate to your CORRECT project directory (where API.py is located)
cd "D:\Data Project\Launching Rocket\rocket-launch"

REM 3. Run your Python script
python LL2_API.py

REM 4. Display a message and pause briefly for confirmation
echo.
echo Data collection attempt finished.
timeout 5