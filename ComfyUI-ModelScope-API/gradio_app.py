import gradio as gr
import requests
import json
import time
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import tempfile
import os
import random
import hashlib

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
    key_file = os.path.join(os.path.dirname(__file__), '.token_key')
    
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
        token_file = os.path.join(os.path.dirname(__file__), '.api_token')
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
        token_file = os.path.join(os.path.dirname(__file__), '.api_token')
        
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
        token_file = os.path.join(os.path.dirname(__file__), '.api_token')
        key_file = os.path.join(os.path.dirname(__file__), '.token_key')
        
        if os.path.exists(token_file):
            os.remove(token_file)
        if os.path.exists(key_file):
            os.remove(key_file)
        
        print("✅ API Token已删除")
        return True
        
    except Exception as e:
        print(f"❌ 删除API Token失败: {e}")
        return False

# 获取图像尺寸信息
def get_image_info(image):
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

# 加载配置文件
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'modelscope_config.json')
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

# 带有重试机制的API请求函数
def make_api_request_with_retry(url, headers, data=None, timeout=60, max_retries=3, base_delay=2, method='post'):
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

# 计算自适应尺寸
def calculate_adaptive_size(image, long_edge):
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

# 图像编辑功能
def edit_image(api_token, model, image, prompt, negative_prompt, adaptive_ratio, width, height, long_edge, steps, guidance, seed):
    config = load_config()
    
    if not api_token:
        return None, "请提供有效的API Token"
    
    if image is None:
        return None, "请先上传图像"
    
    try:
        # 转换上传的图片为base64
        if hasattr(image, 'shape'):  # numpy array
            pil_image = Image.fromarray(image.astype('uint8'))
        else:  # PIL Image
            pil_image = image
        
        # 根据自适应比例选项计算最终尺寸
        if adaptive_ratio:
            final_width, final_height = calculate_adaptive_size(image, long_edge)
        else:
            final_width, final_height = width, height
        
        # 保存图像到临时文件
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            pil_image.save(tmp_file.name, format='JPEG')
            temp_img_path = tmp_file.name
        
        # 上传图片到临时CDN获取URL
        upload_url = 'https://ai.kefan.cn/api/upload/local'
        
        try:
            with open(temp_img_path, 'rb') as img_file:
                files = {'file': img_file}
                upload_response = requests.post(upload_url, files=files)
        finally:
            # 确保文件句柄关闭后再删除
            try:
                os.unlink(temp_img_path)
            except:
                pass
        
        if upload_response.status_code != 200:
            return None, f"图片上传失败: {upload_response.text}"
        
        upload_data = upload_response.json()
        if not upload_data.get('success'):
            return None, f"图片上传失败: {upload_data.get('message', 'Unknown error')}"
        
        image_url = upload_data['data']
        
        # 构建API请求
        payload = {
            'model': model,
            'prompt': prompt,
            'image_url': image_url,
            'size': f"{final_width}x{final_height}",
            'steps': steps,
            'guidance': guidance,
            'seed': seed
        }
        
        if negative_prompt.strip():
            payload['negative_prompt'] = negative_prompt
        
        url = 'https://api-inference.modelscope.cn/v1/images/generations'
        
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
            'X-ModelScope-Async-Mode': 'true'
        }
        
        # 发送API请求
        response = make_api_request_with_retry(
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=int(config.get("timeout", 720)),
            max_retries=2,
            base_delay=3,
            method='post'
        )
        
        if not response:
            return None, "API请求失败: 网络连接问题"
        
        if response.status_code != 200:
            return None, f"API请求失败: {response.status_code}, {response.text}"
        
        task_data = response.json()
        if 'task_id' not in task_data:
            return None, f"API响应格式错误: {task_data}"
        
        task_id = task_data['task_id']
        print(f"任务已提交，任务ID: {task_id}")
        
        # 轮询任务状态
        max_wait_seconds = max(60, int(config.get('timeout', 720)))
        start_time = time.time()
        check_interval = 3
        
        while time.time() - start_time < max_wait_seconds:
            time.sleep(check_interval)
            
            status_response = make_api_request_with_retry(
                url=f'https://api-inference.modelscope.cn/v1/tasks/{task_id}',
                headers={
                    'Authorization': f'Bearer {api_token}',
                    'X-ModelScope-Task-Type': 'image_generation'
                },
                method='get',
                timeout=int(config.get("timeout", 720))
            )
            
            if not status_response:
                continue
                
            if status_response.status_code != 200:
                continue
                
            status_data = status_response.json()
            status = status_data.get('task_status')
            
            if status == 'SUCCEED':
                output_images = status_data.get('output_images', [])
                if not output_images:
                    return None, "任务成功但无输出图像"
                
                # 下载生成的图片
                img_url = output_images[0]
                img_response = requests.get(img_url, timeout=int(config.get("image_download_timeout", 30)))
                
                if img_response.status_code == 200:
                    img_data = BytesIO(img_response.content)
                    result_image = Image.open(img_data)
                    return result_image, f"图像编辑成功！任务ID: {task_id}, 尺寸: {final_width}x{final_height}"
                else:
                    return None, f"图片下载失败: {img_response.status_code}"
            
            elif status == 'FAILED':
                error_info = status_data.get('errors', {})
                return None, f"任务失败: {error_info.get('message', 'Unknown error')}"
            
            elif status == 'PENDING' or status == 'RUNNING':
                continue
        
        return None, "任务轮询超时，请稍后重试"
        
    except Exception as e:
        return None, f"处理过程中发生错误: {str(e)}"

# 文生图功能
def generate_image(api_token, model, prompt, negative_prompt, width, height, steps, guidance, seed):
    config = load_config()
    
    if not api_token:
        return None, "请提供有效的API Token"
    
    try:
        payload = {
            'model': model,
            'prompt': prompt,
            'size': f"{width}x{height}",
            'steps': steps,
            'guidance': guidance,
            'seed': seed
        }
        
        if negative_prompt.strip():
            payload['negative_prompt'] = negative_prompt
        
        url = 'https://api-inference.modelscope.cn/v1/images/generations'
        
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
            'X-ModelScope-Async-Mode': 'true'
        }
        
        response = make_api_request_with_retry(
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=int(config.get("timeout", 720)),
            max_retries=2,
            base_delay=3,
            method='post'
        )
        
        if not response:
            return None, "API请求失败: 网络连接问题"
        
        if response.status_code != 200:
            return None, f"API请求失败: {response.status_code}, {response.text}"
        
        task_data = response.json()
        if 'task_id' not in task_data:
            return None, f"API响应格式错误: {task_data}"
        
        task_id = task_data['task_id']
        print(f"任务已提交，任务ID: {task_id}")
        
        # 轮询任务状态
        max_wait_seconds = max(60, int(config.get('timeout', 720)))
        start_time = time.time()
        check_interval = 3
        
        while time.time() - start_time < max_wait_seconds:
            time.sleep(check_interval)
            
            status_response = make_api_request_with_retry(
                url=f'https://api-inference.modelscope.cn/v1/tasks/{task_id}',
                headers={
                    'Authorization': f'Bearer {api_token}',
                    'X-ModelScope-Task-Type': 'image_generation'
                },
                method='get',
                timeout=int(config.get("timeout", 720))
            )
            
            if not status_response:
                continue
                
            if status_response.status_code != 200:
                continue
                
            status_data = status_response.json()
            status = status_data.get('task_status')
            
            if status == 'SUCCEED':
                output_images = status_data.get('output_images', [])
                if not output_images:
                    return None, "任务成功但无输出图像"
                
                # 下载生成的图片
                img_url = output_images[0]
                img_response = requests.get(img_url, timeout=int(config.get("image_download_timeout", 30)))
                
                if img_response.status_code == 200:
                    img_data = BytesIO(img_response.content)
                    result_image = Image.open(img_data)
                    return result_image, f"图像生成成功！任务ID: {task_id}"
                else:
                    return None, f"图片下载失败: {img_response.status_code}"
            
            elif status == 'FAILED':
                error_info = status_data.get('errors', {})
                return None, f"任务失败: {error_info.get('message', 'Unknown error')}"
            
            elif status == 'PENDING' or status == 'RUNNING':
                continue
        
        return None, "任务轮询超时，请稍后重试"
        
    except Exception as e:
        return None, f"处理过程中发生错误: {str(e)}"

# 文本对话功能
def chat_with_model(message, history, api_token, model, system_prompt, max_tokens, temperature):
    if not OPENAI_AVAILABLE:
        return history + [{"role": "assistant", "content": "请先安装openai库: pip install openai"}], ""
    
    config = load_config()
    
    if not api_token:
        return history + [{"role": "assistant", "content": "请提供有效的API Token"}], ""
    
    if not message.strip():
        return history, ""
    
    try:
        client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key=api_token
        )
        
        # 构建消息历史
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加历史对话（从messages格式转换）
        for msg in history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                if msg["role"] in ["user", "assistant"] and not msg["content"].startswith("系统"):
                    messages.append(msg)
        
        # 添加当前消息
        messages.append({"role": "user", "content": message})
        
        print(f"💬 发送对话请求，模型: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=False
        )
        
        assistant_response = response.choices[0].message.content
        
        # 更新历史记录（使用messages格式）
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": assistant_response}
        ]
        
        return new_history, ""
        
    except Exception as e:
        error_msg = f"对话失败: {str(e)}"
        return history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": error_msg}
        ], ""

# 图生文功能
def analyze_image_with_text(image, prompt, api_token, model, max_tokens, temperature):
    if not OPENAI_AVAILABLE:
        return "请先安装openai库: pip install openai"
    
    if not api_token:
        return "请提供有效的API Token"
    
    if image is None:
        return "请先上传图像"
    
    try:
        print(f"🔍 开始分析图像...")
        print(f"📝 提示词: {prompt}")
        print(f"🤖 模型: {model}")
        
        # 转换图像为base64
        if hasattr(image, 'shape'):  # numpy array
            if image.max() <= 1.0:
                image_np = (image * 255).astype(np.uint8)
            else:
                image_np = image.astype(np.uint8)
            pil_image = Image.fromarray(image_np)
        else:  # PIL Image
            pil_image = image
        
        # 确保图像是RGB格式
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG", quality=85)
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{img_base64}"
        
        print(f"🖼️ 图像已转换为base64格式")
        
        client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key=api_token
        )
        
        messages = [{
            'role': 'user',
            'content': [{
                'type': 'text',
                'text': prompt,
            }, {
                'type': 'image_url',
                'image_url': {
                    'url': image_url,
                },
            }],
        }]
        
        print(f"🚀 发送API请求...")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=False
        )
        
        description = response.choices[0].message.content
        print(f"✅ 分析完成!")
        print(f"📄 结果: {description[:100] if description else 'None'}...")
        
        if not description:
            return "API返回了空的响应，请检查模型是否支持图像分析功能"
        
        return description
        
    except Exception as e:
        error_msg = f"图像分析失败: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

# 创建Gradio界面
def create_gradio_interface():
    config = load_config()
    saved_token = load_api_token()  # 加载保存的token
    
    with gr.Blocks(title="ModelScope API WebUI", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# ModelScope API WebUI")
        gr.Markdown("使用魔搭ModelScope API进行图像生成和编辑")
        
        with gr.Tab("文生图"):
            with gr.Row():
                with gr.Column(scale=1):
                    api_token_gen = gr.Textbox(
                        label="API Token",
                        placeholder="请输入您的ModelScope API Token",
                        type="password",
                        value=saved_token
                    )
                    save_token_gen = gr.Checkbox(
                        label="保存API Token到本地加密文件",
                        value=bool(saved_token)
                    )
                    model_gen = gr.Dropdown(
                        label="模型",
                        choices=config.get("image_models", ["Qwen/Qwen-Image"]),
                        value=config.get("default_model", "Qwen/Qwen-Image")
                    )
                    prompt_gen = gr.Textbox(
                        label="提示词",
                        placeholder="请输入图像描述",
                        value=config.get("default_prompt", "A beautiful landscape"),
                        lines=3
                    )
                    negative_prompt_gen = gr.Textbox(
                        label="负面提示词",
                        placeholder="不希望出现在图像中的内容",
                        value=config.get("default_negative_prompt", ""),
                        lines=2
                    )
                    
                    with gr.Row():
                        width_gen = gr.Slider(label="宽度", minimum=256, maximum=2048, value=config.get("default_width", 512), step=64)
                        height_gen = gr.Slider(label="高度", minimum=256, maximum=2048, value=config.get("default_height", 512), step=64)
                    
                    with gr.Row():
                        steps_gen = gr.Slider(label="步数", minimum=1, maximum=100, value=config.get("default_steps", 30), step=1)
                        guidance_gen = gr.Slider(label="引导系数", minimum=1.0, maximum=20.0, value=config.get("default_guidance", 7.5), step=0.1)
                        seed_gen = gr.Number(label="随机种子", value=config.get("default_seed", -1))
                
                with gr.Column(scale=1):
                    output_image_gen = gr.Image(label="生成结果", type="pil")
                    output_message_gen = gr.Textbox(label="输出信息", interactive=False)
                    gen_btn = gr.Button("生成图像", variant="primary")
        
        with gr.Tab("图像编辑"):
            with gr.Row():
                with gr.Column(scale=1):
                    api_token_edit = gr.Textbox(
                        label="API Token",
                        placeholder="请输入您的ModelScope API Token",
                        type="password",
                        value=saved_token
                    )
                    save_token_edit = gr.Checkbox(
                        label="保存API Token到本地加密文件",
                        value=bool(saved_token)
                    )
                    model_edit = gr.Dropdown(
                        label="模型",
                        choices=config.get("image_edit_models", ["Qwen/Qwen-Image-Edit"]),
                        value=config.get("image_edit_models", ["Qwen/Qwen-Image-Edit"])[0] if config.get("image_edit_models") else "Qwen/Qwen-Image-Edit"
                    )
                    input_image_edit = gr.Image(label="输入图像", type="pil")
                    input_image_info_edit = gr.Textbox(label="输入图像信息", interactive=False, visible=False)
                    prompt_edit = gr.Textbox(
                        label="提示词",
                        placeholder="请输入图像编辑描述",
                        value="修改图片中的内容",
                        lines=3
                    )
                    negative_prompt_edit = gr.Textbox(
                        label="负面提示词",
                        placeholder="不希望出现在图像中的内容",
                        value=config.get("default_negative_prompt", ""),
                        lines=2
                    )
                    
                    adaptive_ratio_edit = gr.Checkbox(
                        label="自适应原图比例",
                        value=True,
                        info="勾选后只需调整长边尺寸，自动保持原图比例"
                    )
                    
                    with gr.Row():
                        with gr.Column(visible=False) as manual_size_edit:
                            width_edit = gr.Slider(label="宽度", minimum=256, maximum=2048, value=config.get("default_width", 512), step=64)
                            height_edit = gr.Slider(label="高度", minimum=256, maximum=2048, value=config.get("default_height", 512), step=64)
                        
                        with gr.Column(visible=True) as adaptive_size_edit:
                            long_edge_edit = gr.Slider(label="长边尺寸", minimum=256, maximum=2048, value=1024, step=64, info="图像长边的像素尺寸，短边会自动按原图比例计算")
                    
                    with gr.Row():
                        steps_edit = gr.Slider(label="步数", minimum=1, maximum=100, value=config.get("default_steps", 30), step=1)
                        guidance_edit = gr.Slider(label="引导系数", minimum=1.0, maximum=20.0, value=config.get("default_guidance", 7.5), step=0.1)
                        seed_edit = gr.Number(label="随机种子", value=config.get("default_seed", -1))
                
                with gr.Column(scale=1):
                    output_image_edit = gr.Image(label="编辑结果", type="pil")
                    output_message_edit = gr.Textbox(label="输出信息", interactive=False)
                    edit_btn = gr.Button("编辑图像", variant="primary")
        
        with gr.Tab("文本对话"):
            with gr.Row():
                with gr.Column(scale=1):
                    api_token_chat = gr.Textbox(
                        label="API Token",
                        placeholder="请输入您的ModelScope API Token",
                        type="password",
                        value=saved_token
                    )
                    save_token_chat = gr.Checkbox(
                        label="保存API Token到本地加密文件",
                        value=bool(saved_token)
                    )
                    model_chat = gr.Dropdown(
                        label="模型",
                        choices=config.get("text_models", ["Qwen/Qwen3-Coder-480B-A35B-Instruct"]),
                        value=config.get("default_text_model", "Qwen/Qwen3-Coder-480B-A35B-Instruct")
                    )
                    system_prompt_chat = gr.Textbox(
                        label="系统提示词",
                        placeholder="设置AI的角色和行为",
                        value=config.get("default_system_prompt", "You are a helpful assistant."),
                        lines=2
                    )
                    
                    with gr.Row():
                        max_tokens_chat = gr.Slider(label="最大Token数", minimum=100, maximum=8000, value=2000, step=100)
                        temperature_chat = gr.Slider(label="温度", minimum=0.1, maximum=2.0, value=0.7, step=0.1)
                
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(label="对话历史", height=400, type="messages")
                    msg = gr.Textbox(label="输入消息", placeholder="请输入您的问题...", lines=2)
                    with gr.Row():
                        submit_btn = gr.Button("发送", variant="primary")
                        clear_btn = gr.Button("清空对话")
        
        with gr.Tab("图生文"):
            with gr.Row():
                with gr.Column(scale=1):
                    api_token_vision = gr.Textbox(
                        label="API Token",
                        placeholder="请输入您的ModelScope API Token",
                        type="password",
                        value=saved_token
                    )
                    save_token_vision = gr.Checkbox(
                        label="保存API Token到本地加密文件",
                        value=bool(saved_token)
                    )
                    model_vision = gr.Dropdown(
                        label="模型",
                        choices=config.get("vision_models", ["stepfun-ai/step3"]),
                        value=config.get("vision_models", ["stepfun-ai/step3"])[0] if config.get("vision_models") else "stepfun-ai/step3"
                    )
                    input_image_vision = gr.Image(label="输入图像", type="pil")
                    input_image_info_vision = gr.Textbox(label="输入图像信息", interactive=False, visible=False)
                    prompt_vision = gr.Textbox(
                        label="提示词",
                        placeholder="请输入您想了解图像的什么信息",
                        value="请详细描述这幅图像的内容",
                        lines=3
                    )
                    
                    with gr.Row():
                        max_tokens_vision = gr.Slider(label="最大Token数", minimum=100, maximum=4000, value=1000, step=100)
                        temperature_vision = gr.Slider(label="温度", minimum=0.1, maximum=2.0, value=0.7, step=0.1)
                
                with gr.Column(scale=1):
                    output_text_vision = gr.Textbox(label="图像描述", lines=15, interactive=False)
                    analyze_btn = gr.Button("分析图像", variant="primary")
        
        # API Token保存处理函数
        def handle_token_save(token, should_save):
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
        
        # 界面切换逻辑
        def toggle_size_controls(adaptive_ratio):
            if adaptive_ratio:
                return gr.update(visible=False), gr.update(visible=True)
            else:
                return gr.update(visible=True), gr.update(visible=False)
        
        adaptive_ratio_edit.change(
            fn=toggle_size_controls,
            inputs=[adaptive_ratio_edit],
            outputs=[manual_size_edit, adaptive_size_edit]
        )
        
        # 图像尺寸显示事件
        def update_image_info(image):
            if image is None:
                return gr.update(visible=False), ""
            else:
                info = get_image_info(image)
                return gr.update(visible=True), info
        
        # 添加状态显示组件
        with gr.Row():
            token_status = gr.Textbox(label="Token状态", interactive=False, visible=False)
        
        # API Token保存事件绑定
        save_token_gen.change(
            fn=handle_token_save,
            inputs=[api_token_gen, save_token_gen],
            outputs=[token_status]
        )
        
        save_token_edit.change(
            fn=handle_token_save,
            inputs=[api_token_edit, save_token_edit],
            outputs=[token_status]
        )
        
        save_token_chat.change(
            fn=handle_token_save,
            inputs=[api_token_chat, save_token_chat],
            outputs=[token_status]
        )
        
        save_token_vision.change(
            fn=handle_token_save,
            inputs=[api_token_vision, save_token_vision],
            outputs=[token_status]
        )
        
        # 绑定事件
        gen_btn.click(
            fn=generate_image,
            inputs=[api_token_gen, model_gen, prompt_gen, negative_prompt_gen, width_gen, height_gen, steps_gen, guidance_gen, seed_gen],
            outputs=[output_image_gen, output_message_gen]
        )
        
        edit_btn.click(
            fn=edit_image,
            inputs=[api_token_edit, model_edit, input_image_edit, prompt_edit, negative_prompt_edit, adaptive_ratio_edit, width_edit, height_edit, long_edge_edit, steps_edit, guidance_edit, seed_edit],
            outputs=[output_image_edit, output_message_edit]
        )
        
        # 输入图像变化时显示尺寸信息
        input_image_edit.change(
            fn=update_image_info,
            inputs=[input_image_edit],
            outputs=[input_image_info_edit, input_image_info_edit]
        )
        
        input_image_vision.change(
            fn=update_image_info,
            inputs=[input_image_vision],
            outputs=[input_image_info_vision, input_image_info_vision]
        )
        
        # 文本对话事件绑定
        def clear_chat():
            return [], ""
        
        submit_btn.click(
            fn=chat_with_model,
            inputs=[msg, chatbot, api_token_chat, model_chat, system_prompt_chat, max_tokens_chat, temperature_chat],
            outputs=[chatbot, msg]
        )
        
        msg.submit(
            fn=chat_with_model,
            inputs=[msg, chatbot, api_token_chat, model_chat, system_prompt_chat, max_tokens_chat, temperature_chat],
            outputs=[chatbot, msg]
        )
        
        clear_btn.click(
            fn=clear_chat,
            outputs=[chatbot, msg]
        )
        
        # 图生文事件绑定
        analyze_btn.click(
            fn=analyze_image_with_text,
            inputs=[input_image_vision, prompt_vision, api_token_vision, model_vision, max_tokens_vision, temperature_vision],
            outputs=[output_text_vision]
        )
        
        # 添加简单的JavaScript代码用于界面增强
        demo.load(js="""
        function() {
            console.log('ModelScope API WebUI loaded');
            
            // 添加一些界面增强功能
            setTimeout(function() {
                // 为所有按钮添加加载状态样式
                const buttons = document.querySelectorAll('button');
                buttons.forEach(button => {
                    button.addEventListener('click', function() {
                        if (this.textContent.includes('生成') || this.textContent.includes('编辑') || this.textContent.includes('分析')) {
                            this.style.opacity = '0.7';
                            setTimeout(() => {
                                this.style.opacity = '1';
                            }, 1000);
                        }
                    });
                });
            }, 1000);
        }
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)