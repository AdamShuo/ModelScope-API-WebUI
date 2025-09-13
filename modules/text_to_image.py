"""
文生图模块
处理文本到图像的生成功能
"""

import json
import time
import requests
from PIL import Image
from io import BytesIO
from .common import load_config, make_api_request_with_retry

def generate_image(api_token, model, prompt, negative_prompt, width, height, steps, guidance, seed):
    """文生图功能"""
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