@echo off
echo ========================================
echo ModelScope API WebUI 安装程序 (Windows)
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python环境
    echo.
    echo 请先安装Python 3.8或更高版本：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装Python
    echo 3. 安装时勾选"Add Python to PATH"选项
    echo.
    pause
    exit /b 1
)

echo ✅ 检测到Python环境
python --version

echo.
echo 开始安装依赖...
echo.

REM 创建虚拟环境
if not exist ".venv" (
    echo 创建虚拟环境...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ❌ 虚拟环境创建失败
        pause
        exit /b 1
    )
)

echo 激活虚拟环境并安装依赖...
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ 安装完成！
    echo.
    echo 启动应用：
    echo 1. 双击运行 run_windows_smart.bat
    echo 2. 或在命令行执行：run_windows_smart.bat
    echo.
    echo 应用将在浏览器中自动打开
    echo.
) else (
    echo.
    echo ❌ 依赖安装失败，请检查网络连接
    echo.
)

pause