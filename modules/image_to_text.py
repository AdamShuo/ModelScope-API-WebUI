"""
图生文模块
处理图像分析和描述功能
"""

import base64
import numpy as np
from PIL import Image
from io import BytesIO
from .common import OPENAI_AVAILABLE, OpenAI

def analyze_image_with_text(image, prompt, api_token, model, max_tokens, temperature):
    """图生文功能"""
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