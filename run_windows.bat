@echo off
chcp 65001 >nul
echo Starting ModelScope API WebUI...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found, creating... / 虚拟环境不存在，正在创建...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment, please check Python installation / 创建虚拟环境失败，请检查Python安装
        pause
        exit /b 1
    )
    echo Virtual environment created successfully / 虚拟环境创建成功
    
    REM Activate virtual environment
    echo Activating virtual environment... / 正在激活虚拟环境...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo Failed to activate virtual environment / 激活虚拟环境失败
        pause
        exit /b 1
    )
    
    REM Install dependencies if needed
    if exist "requirements.txt" (
        echo Installing dependencies... / 正在安装依赖包...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo Failed to install dependencies / 安装依赖包失败
            pause
            exit /b 1
        )
        echo Dependencies installed successfully / 依赖包安装成功
    )
) else (
    echo Virtual environment already exists / 虚拟环境已存在
    echo Activating virtual environment... / 正在激活虚拟环境...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo Failed to activate virtual environment / 激活虚拟环境失败
        pause
        exit /b 1
    )
    echo Virtual environment activated successfully / 虚拟环境激活成功
    
    REM Check if dependencies are already installed
    echo Checking if dependencies are installed... / 检查依赖包是否已安装...
    pip list | findstr "gradio" >nul
    if errorlevel 1 (
        echo Installing dependencies... / 正在安装依赖包...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo Failed to install dependencies / 安装依赖包失败
            pause
            exit /b 1
        )
        echo Dependencies installed successfully / 依赖包安装成功
    ) else (
        echo Dependencies already installed / 依赖包已安装
    )
)

REM Run the application
echo.
echo Starting application... / 正在启动应用程序...
echo Application will start at http://127.0.0.1:7860 / 应用将在 http://127.0.0.1:7860 启动
echo Browser will open automatically with dark theme... / 浏览器将自动打开深色主题...
echo.

REM Start application in background and open browser with dark theme
echo Waiting for application to start... / 等待应用程序启动...
start /B python gradio_app.py
timeout /t 8 /nobreak >nul
start http://127.0.0.1:7860/?__theme=dark

REM Wait for user input to close
echo.
echo ========================================
echo  Application is running / 应用程序正在运行
echo  Press ANY KEY to EXIT / 按任意键退出程序
echo ========================================
pause >nul

echo.
echo Stopping application... / 正在停止应用程序...
REM Kill the Python process
taskkill /f /im python.exe >nul 2>&1
echo Application stopped / 应用程序已停止

REM Pause after program ends
echo.
echo Application ended
pause