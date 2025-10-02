#!/bin/bash
echo "========================================"
echo "ModelScope API WebUI 安装程序 (Linux)"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到Python3环境"
    echo
    echo "请先安装Python 3.8或更高版本："
    echo "Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Arch Linux: sudo pacman -S python python-pip"
    echo
    exit 1
fi

echo "✅ 检测到Python环境"
python3 --version

echo
echo "开始安装依赖..."
echo

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
fi

echo "激活虚拟环境并安装依赖..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "✅ 安装完成！"
    echo
    echo "启动应用："
    echo "1. 执行: ./run_linux_smart.sh"
    echo "2. 或执行: bash run_linux_smart.sh"
    echo
    echo "应用将在浏览器中自动打开"
    echo
else
    echo
    echo "❌ 依赖安装失败，请检查网络连接"
    echo
fi