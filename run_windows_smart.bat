@echo off
chcp 65001 >nul
echo Starting ModelScope API WebUI (Smart Mode)...
echo.

REM 检测Python是否可用
echo Checking Python availability... / 正在检查Python可用性...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is available, using system Python / Python可用，使用系统Python
    set PYTHON_CMD=python
) else (
    echo Python not found in system PATH / 系统中未找到Python
    echo Checking virtual environment Python... / 正在检查虚拟环境中的Python...
    if exist ".venv\Scripts\python.exe" (
        echo Using virtual environment Python / 使用虚拟环境中的Python
        set PYTHON_CMD=.venv\Scripts\python.exe
    ) else (
        echo ERROR: No Python found and virtual environment doesn't exist / 错误：未找到Python且虚拟环境不存在
        echo.
        echo Please install Python 3.8+ from https://python.org or run setup script / 请从 https://python.org 安装Python 3.8+ 或运行安装脚本
        echo.
        pause
        exit /b 1
    )
)

REM 检查虚拟环境是否存在
if not exist ".venv" (
    echo Virtual environment not found, creating... / 虚拟环境不存在，正在创建...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment / 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo Virtual environment created successfully / 虚拟环境创建成功
    
    REM 激活虚拟环境
    echo Activating virtual environment... / 正在激活虚拟环境...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo Failed to activate virtual environment / 激活虚拟环境失败
        pause
        exit /b 1
    )
    
    REM 安装依赖
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
    
    REM 检查依赖是否已安装
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

REM 运行应用程序
echo.
echo Starting application... / 正在启动应用程序...
echo Application will start at http://127.0.0.1:7860 / 应用将在 http://127.0.0.1:7860 启动
echo Browser will open automatically with dark theme... / 浏览器将自动打开深色主题...
echo.

REM 启动应用程序并在后台运行
echo Waiting for application to start... / 等待应用程序启动...
start /B python gradio_app.py
timeout /t 8 /nobreak >nul
start http://127.0.0.1:7860/?__theme=dark

REM 等待用户输入关闭
echo.
echo ========================================
echo  Application is running / 应用程序正在运行
echo  Press ANY KEY to EXIT / 按任意键退出程序
echo ========================================
pause >nul

echo.
echo Stopping application... / 正在停止应用程序...
REM 终止Python进程
taskkill /f /im python.exe >nul 2>&1
echo Application stopped / 应用程序已停止

REM 程序结束后暂停
echo.
echo Application ended
pause