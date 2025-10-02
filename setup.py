#!/usr/bin/env python3
"""
ModelScope API WebUI 安装脚本
用于在没有Python环境的系统上设置项目环境
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
import shutil

def detect_platform():
    """检测操作系统平台"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        return "unknown"

def download_python_windows():
    """为Windows下载Python安装包"""
    python_url = "https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe"
    installer_path = "python_installer.exe"
    
    print("正在下载Python 3.12.7安装包...")
    try:
        urllib.request.urlretrieve(python_url, installer_path)
        print("下载完成")
        return installer_path
    except Exception as e:
        print(f"下载失败: {e}")
        return None

def install_python_windows(installer_path):
    """安装Python（Windows）"""
    print("正在安装Python...")
    try:
        # 静默安装Python，添加到PATH
        subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)
        print("Python安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Python安装失败: {e}")
        return False

def setup_environment():
    """设置项目环境"""
    print("正在设置项目环境...")
    
    # 检查Python是否可用
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
        python_available = True
    except:
        python_available = False
    
    if not python_available:
        print("错误：Python不可用")
        return False
    
    # 创建虚拟环境
    print("创建虚拟环境...")
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("虚拟环境创建成功")
    except subprocess.CalledProcessError as e:
        print(f"虚拟环境创建失败: {e}")
        return False
    
    # 激活虚拟环境并安装依赖
    if platform.system().lower() == "windows":
        pip_path = ".venv\\Scripts\\pip.exe"
    else:
        pip_path = ".venv/bin/pip"
    
    print("安装依赖包...")
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("依赖包安装成功")
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败: {e}")
        return False
    
    return True

def main():
    print("=" * 50)
    print("ModelScope API WebUI 环境安装程序")
    print("=" * 50)
    
    current_platform = detect_platform()
    print(f"检测到操作系统: {current_platform}")
    
    # 检查Python是否已安装
    try:
        subprocess.run(["python", "--version"], check=True, capture_output=True)
        print("Python已安装")
        python_installed = True
    except:
        python_installed = False
    
    if not python_installed:
        print("未检测到Python安装")
        if current_platform == "windows":
            print("正在为Windows系统下载Python...")
            installer_path = download_python_windows()
            if installer_path and install_python_windows(installer_path):
                print("Python安装成功")
                # 清理安装包
                if os.path.exists(installer_path):
                    os.remove(installer_path)
            else:
                print("请手动安装Python: https://python.org")
                return
        else:
            print("请手动安装Python:")
            print("Ubuntu/Debian: sudo apt install python3 python3-pip")
            print("CentOS/RHEL: sudo yum install python3 python3-pip") 
            print("macOS: brew install python")
            return
    
    # 设置项目环境
    if setup_environment():
        print("=" * 50)
        print("环境设置完成！")
        print("现在您可以运行以下命令启动应用:")
        if current_platform == "windows":
            print("run_windows_smart.bat")
        else:
            print("./run_linux_smart.sh")
        print("=" * 50)
    else:
        print("环境设置失败，请检查错误信息")

if __name__ == "__main__":
    main()