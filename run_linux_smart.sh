#!/bin/bash

echo "Starting ModelScope API WebUI (Smart Mode)... / 正在启动 ModelScope API WebUI (智能模式)..."
echo

# 检测Python是否可用
echo "Checking Python availability... / 正在检查Python可用性..."
if command -v python3 &> /dev/null; then
    echo "Python3 is available, using system Python / Python3可用，使用系统Python"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    echo "Python is available, using system Python / Python可用，使用系统Python"
    PYTHON_CMD="python"
else
    echo "Python not found in system PATH / 系统中未找到Python"
    echo "Checking virtual environment Python... / 正在检查虚拟环境中的Python..."
    if [ -f ".venv/bin/python" ]; then
        echo "Using virtual environment Python / 使用虚拟环境中的Python"
        PYTHON_CMD=".venv/bin/python"
    else
        echo "ERROR: No Python found and virtual environment doesn't exist / 错误：未找到Python且虚拟环境不存在"
        echo
        echo "Please install Python 3.8+ or run setup script / 请安装Python 3.8+ 或运行安装脚本"
        echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "macOS: brew install python"
        echo
        exit 1
    fi
fi

# 检查虚拟环境是否存在
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found, creating... / 虚拟环境不存在，正在创建..."
    $PYTHON_CMD -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment / 创建虚拟环境失败"
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