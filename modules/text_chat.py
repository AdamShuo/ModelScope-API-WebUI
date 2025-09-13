"""
文本对话模块
处理与AI模型的文本对话功能
"""

from .common import load_config, OPENAI_AVAILABLE, OpenAI

def chat_with_model(message, history, api_token, model, system_prompt, max_tokens, temperature):
    """文本对话功能"""
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

def clear_chat():
    """清空对话历史"""
    return [], ""