@echo off
echo Setting up virtual environment...

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed. Please install Python 3.6 or later and try again.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
call venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Warning: Failed to upgrade pip. Continuing with installation...
)

:: Install Gradio, Pillow, and Requests
echo Installing Gradio, Pillow, and Requests...
pip install gradio pillow requests >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install Gradio, Pillow, or Requests.
    call venv\Scripts\deactivate
    pause
    exit /b 1
)

:: Check if app.py exists
if not exist app.py (
    echo Error: app.py not found in the current directory. Please ensure app.py is present.
    call venv\Scripts\deactivate
    pause
    exit /b 1
)

:: Run the Gradio app
echo Starting the Gradio app at http://localhost:7860...
python app.py
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to start the Gradio app. Check app.py for errors.
    call venv\Scripts\deactivate
    pause
    exit /b 1
)

:: Deactivate virtual environment
call venv\Scripts\deactivate
pause