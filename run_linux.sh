#!/bin/bash

echo "Starting ModelScope API WebUI..."
echo

# 检查虚拟环境是否存在
if [ ! -d ".venv" ]; then
    echo "虚拟环境不存在，正在创建..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "创建虚拟环境失败，请检查Python是否正确安装"
        exit 1
    fi
    echo "虚拟环境创建成功"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "激活虚拟环境失败"
    exit 1
fi

# 检查是否需要安装依赖
if [ -f "requirements.txt" ]; then
    echo "检查并安装依赖包..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "安装依赖包失败"
        exit 1
    fi
fi

# 运行程序
echo
echo "启动应用程序..."
python gradio_app.py

echo
echo "程序已结束"