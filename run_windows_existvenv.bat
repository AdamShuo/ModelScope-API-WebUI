@echo off
echo Starting ModelScope API WebUI...
echo.

REM 激活虚拟环境
echo 激活虚拟环境...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo 激活虚拟环境失败
    pause
    exit /b 1
)

REM 运行程序
echo.
echo 启动应用程序...
python gradio_app.py

REM 程序结束后暂停，以便查看输出
echo.
echo 程序已结束
pause