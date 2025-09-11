#!/bin/bash

echo "Starting ModelScope API WebUI... / 正在启动 ModelScope API WebUI..."
echo

# 检查虚拟环境是否存在
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found, creating... / 虚拟环境不存在，正在创建..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment, please check if Python is installed correctly / 创建虚拟环境失败，请检查Python是否正确安装"
        exit 1
    fi
    echo "Virtual environment created successfully / 虚拟环境创建成功"
fi

# 激活虚拟环境
echo "Activating virtual environment... / 正在激活虚拟环境..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment / 激活虚拟环境失败"
    exit 1
fi

# 检查是否需要安装依赖
if [ -f "requirements.txt" ]; then
    echo "Checking and installing dependencies... / 正在检查并安装依赖包..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies / 安装依赖包失败"
        exit 1
    fi
fi

# 运行程序 / Run the application
echo
echo "Starting application... / 正在启动应用程序..."
echo "Application will start at http://127.0.0.1:7860 / 应用将在 http://127.0.0.1:7860 启动"
echo "Browser will open automatically with dark theme... / 浏览器将自动打开深色主题..."
echo

# 启动应用程序并在后台运行
echo "Waiting for application to start... / 等待应用程序启动..."
python gradio_app.py &
APP_PID=$!

# 等待应用启动
sleep 8

# 打开浏览器并使用深色主题
if command -v xdg-open > /dev/null; then
    xdg-open "http://127.0.0.1:7860/?__theme=dark"
elif command -v open > /dev/null; then
    open "http://127.0.0.1:7860/?__theme=dark"
else
    echo "Please open http://127.0.0.1:7860/?__theme=dark in your browser"
    echo "请在浏览器中打开 http://127.0.0.1:7860/?__theme=dark"
fi

echo
echo "========================================"
echo " Application is running / 应用程序正在运行"
echo " Press Ctrl+C to EXIT / 按 Ctrl+C 退出程序"
echo "========================================"

# 等待用户中断
wait $APP_PID

echo
echo "Application ended / 应用程序已结束"