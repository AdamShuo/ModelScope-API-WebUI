"""
公共函数和工具模块
包含API Token管理、配置加载、图像处理等通用功能
"""

import os
import json
import time
import base64
import hashlib
import requests
import numpy as np
from PIL import Image

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    print("⚠️ 警告: 未安装cryptography库，将使用简单编码保存API Token")
    print("建议运行: pip install cryptography")
    CRYPTO_AVAILABLE = False
    Fernet = None

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("⚠️ 警告: 未安装openai库，文本对话和图生文功能将不可用")
    print("请运行: pip install openai")
    OPENAI_AVAILABLE = False
    OpenAI = None

# API Token 加密保存和读取功能
def get_encryption_key():
    """生成或获取加密密钥"""
    key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.token_key')
    
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        # 基于机器特征生成密钥
        machine_id = hashlib.sha256(
            (os.getcwd() + str(os.path.getsize(__file__))).encode()
        ).digest()[:32]
        
        if CRYPTO_AVAILABLE:
            key = Fernet.generate_key()
        else:
            # 简单的base64编码作为备选
            key = base64.b64encode(machine_id)
        
        with open(key_file, 'wb') as f:
            f.write(key)
        
        return key

def save_api_token(token):
    """保存API Token到加密文件"""
    if not token or not token.strip():
        return False
    
    try:
        token_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.api_token')
        key = get_encryption_key()
        
        if CRYPTO_AVAILABLE:
            # 使用Fernet加密
            fernet = Fernet(key)
            encrypted_token = fernet.encrypt(token.encode())
        else:
            # 简单的base64编码
            encrypted_token = base64.b64encode(token.encode())
        
        with open(token_file, 'wb') as f:
            f.write(encrypted_token)
        
        print("✅ API Token已保存到本地加密文件")
        return True
        
    except Exception as e:
        print(f"❌ 保存API Token失败: {e}")
        return False

def load_api_token():
    """从加密文件读取API Token"""
    try:
        token_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.api_token')
        
        if not os.path.exists(token_file):
            return ""
        
        key = get_encryption_key()
        
        with open(token_file, 'rb') as f:
            encrypted_token = f.read()
        
        if CRYPTO_AVAILABLE:
            # 使用Fernet解密
            fernet = Fernet(key)
            token = fernet.decrypt(encrypted_token).decode()
        else:
            # 简单的base64解码
            token = base64.b64decode(encrypted_token).decode()
        
        return token
        
    except Exception as e:
        print(f"⚠️ 读取API Token失败: {e}")
        return ""

def delete_api_token():
    """删除保存的API Token"""
    try:
        token_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.api_token')
        key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.token_key')
        
        if os.path.exists(token_file):
            os.remove(token_file)
        if os.path.exists(key_file):
            os.remove(key_file)
        
        print("✅ API Token已删除")
        return True
        
    except Exception as e:
        print(f"❌ 删除API Token失败: {e}")
        return False

def get_image_info(image):
    """获取图像尺寸信息"""
    if image is None:
        return "无图像"
    
    if hasattr(image, 'size'):  # PIL Image
        width, height = image.size
        return f"尺寸: {width} × {height} 像素"
    elif hasattr(image, 'shape'):  # numpy array
        if len(image.shape) == 3:
            height, width = image.shape[:2]
        else:
            height, width = image.shape
        return f"尺寸: {width} × {height} 像素"
    else:
        return "无法获取尺寸信息"

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modelscope_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "default_model": "Qwen/Qwen-Image",
            "timeout": 720,
            "image_download_timeout": 30,
            "default_prompt": "A beautiful landscape"
        }

def make_api_request_with_retry(url, headers, data=None, timeout=60, max_retries=3, base_delay=2, method='post'):
    """带有重试机制的API请求函数"""
    for attempt in range(max_retries):
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, timeout=timeout)
            else:
                response = requests.post(url, data=data, headers=headers, timeout=timeout)
            
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                wait_time = int(retry_after) if retry_after else base_delay * (2 ** attempt)
                print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            
            return response
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = base_delay * (2 ** attempt)
                print(f"Request timeout. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            else:
                print("Max retries reached. Request failed.")
                return None
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = base_delay * (2 ** attempt)
                print(f"Request failed: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            else:
                print(f"Max retries reached. Final error: {e}")
                return None
    
    return None

def calculate_adaptive_size(image, long_edge):
    """计算自适应尺寸"""
    if hasattr(image, 'shape'):  # numpy array
        h, w = image.shape[:2]
    else:  # PIL Image
        w, h = image.size
    
    # 计算比例
    if w >= h:  # 宽图
        new_w = long_edge
        new_h = int(h * long_edge / w)
    else:  # 高图
        new_h = long_edge
        new_w = int(w * long_edge / h)
    
    # 确保尺寸是64的倍数
    new_w = ((new_w + 31) // 64) * 64
    new_h = ((new_h + 31) // 64) * 64
    
    return new_w, new_h

def handle_token_save(token, should_save):
    """API Token保存处理函数"""
    if should_save and token and token.strip():
        success = save_api_token(token)
        if success:
            return "✅ API Token已保存到本地加密文件"
        else:
            return "❌ API Token保存失败"
    elif not should_save:
        delete_api_token()
        return "🗑️ API Token已删除"
    else:
        return ""

def update_image_info(image):
    """图像尺寸显示事件"""
    import gradio as gr
    if image is None:
        return gr.update(visible=False), ""
    else:
        info = get_image_info(image)
        return gr.update(visible=True), info