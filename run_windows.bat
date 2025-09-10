@echo off
echo Starting ModelScope API WebUI...
echo.

REM 检查虚拟环境是否存在
if not exist ".venv" (
    echo 虚拟环境不存在，正在创建...
    python -m venv .venv
    if errorlevel 1 (
        echo 创建虚拟环境失败，请检查Python是否正确安装
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)

REM 激活虚拟环境
echo 激活虚拟环境...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo 激活虚拟环境失败
    pause
    exit /b 1
)

REM 检查是否需要安装依赖
if exist "requirements.txt" (
    echo 检查并安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 安装依赖包失败
        pause
        exit /b 1
    )
)

REM 运行程序
echo.
echo 启动应用程序...
python gradio_app.py

REM 程序结束后暂停，以便查看输出
echo.
echo 程序已结束
pause