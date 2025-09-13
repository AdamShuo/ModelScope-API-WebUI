"""
ModelScope API WebUI - 主应用文件
模块化重构版本，将功能分散到不同的子模块中
"""

import gradio as gr
from modules.common import (
    load_config, 
    load_api_token, 
    handle_token_save, 
    update_image_info
)
from modules.text_to_image import generate_image
from modules.image_edit import edit_image
from modules.text_chat import chat_with_model, clear_chat
from modules.image_to_text import analyze_image_with_text
from modules.photopea import create_photopea_interface

def create_text_to_image_tab(config, saved_token):
    """创建文生图标签页"""
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
        
        return {
            'api_token': api_token_gen,
            'save_token': save_token_gen,
            'model': model_gen,
            'prompt': prompt_gen,
            'negative_prompt': negative_prompt_gen,
            'width': width_gen,
            'height': height_gen,
            'steps': steps_gen,
            'guidance': guidance_gen,
            'seed': seed_gen,
            'output_image': output_image_gen,
            'output_message': output_message_gen,
            'button': gen_btn
        }

def create_image_edit_tab(config, saved_token):
    """创建图像编辑标签页"""
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
        
        return {
            'api_token': api_token_edit,
            'save_token': save_token_edit,
            'model': model_edit,
            'input_image': input_image_edit,
            'input_image_info': input_image_info_edit,
            'prompt': prompt_edit,
            'negative_prompt': negative_prompt_edit,
            'adaptive_ratio': adaptive_ratio_edit,
            'manual_size': manual_size_edit,
            'adaptive_size': adaptive_size_edit,
            'width': width_edit,
            'height': height_edit,
            'long_edge': long_edge_edit,
            'steps': steps_edit,
            'guidance': guidance_edit,
            'seed': seed_edit,
            'output_image': output_image_edit,
            'output_message': output_message_edit,
            'button': edit_btn
        }

def create_text_chat_tab(config, saved_token):
    """创建文本对话标签页"""
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
        
        return {
            'api_token': api_token_chat,
            'save_token': save_token_chat,
            'model': model_chat,
            'system_prompt': system_prompt_chat,
            'max_tokens': max_tokens_chat,
            'temperature': temperature_chat,
            'chatbot': chatbot,
            'msg': msg,
            'submit_btn': submit_btn,
            'clear_btn': clear_btn
        }

def create_image_to_text_tab(config, saved_token):
    """创建图生文标签页"""
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
        
        return {
            'api_token': api_token_vision,
            'save_token': save_token_vision,
            'model': model_vision,
            'input_image': input_image_vision,
            'input_image_info': input_image_info_vision,
            'prompt': prompt_vision,
            'max_tokens': max_tokens_vision,
            'temperature': temperature_vision,
            'output_text': output_text_vision,
            'button': analyze_btn
        }

def create_gradio_interface():
    """创建Gradio界面"""
    config = load_config()
    saved_token = load_api_token()  # 加载保存的token
    
    with gr.Blocks(title="ModelScope API WebUI", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# ModelScope API WebUI")
        gr.Markdown("使用魔搭ModelScope API进行图像生成和编辑")
        
        # 创建各个标签页
        text_to_image_components = create_text_to_image_tab(config, saved_token)
        image_edit_components = create_image_edit_tab(config, saved_token)
        text_chat_components = create_text_chat_tab(config, saved_token)
        image_to_text_components = create_image_to_text_tab(config, saved_token)
        
        # 创建 Photopea 标签页
        create_photopea_interface()
        
        # 界面切换逻辑
        def toggle_size_controls(adaptive_ratio):
            if adaptive_ratio:
                return gr.update(visible=False), gr.update(visible=True)
            else:
                return gr.update(visible=True), gr.update(visible=False)
        
        # 添加状态显示组件
        with gr.Row():
            token_status = gr.Textbox(label="Token状态", interactive=False, visible=False)
        
        # 绑定事件 - 文生图
        text_to_image_components['save_token'].change(
            fn=handle_token_save,
            inputs=[text_to_image_components['api_token'], text_to_image_components['save_token']],
            outputs=[token_status]
        )
        
        text_to_image_components['button'].click(
            fn=generate_image,
            inputs=[
                text_to_image_components['api_token'],
                text_to_image_components['model'],
                text_to_image_components['prompt'],
                text_to_image_components['negative_prompt'],
                text_to_image_components['width'],
                text_to_image_components['height'],
                text_to_image_components['steps'],
                text_to_image_components['guidance'],
                text_to_image_components['seed']
            ],
            outputs=[text_to_image_components['output_image'], text_to_image_components['output_message']]
        )
        
        # 绑定事件 - 图像编辑
        image_edit_components['save_token'].change(
            fn=handle_token_save,
            inputs=[image_edit_components['api_token'], image_edit_components['save_token']],
            outputs=[token_status]
        )
        
        image_edit_components['adaptive_ratio'].change(
            fn=toggle_size_controls,
            inputs=[image_edit_components['adaptive_ratio']],
            outputs=[image_edit_components['manual_size'], image_edit_components['adaptive_size']]
        )
        
        image_edit_components['input_image'].change(
            fn=update_image_info,
            inputs=[image_edit_components['input_image']],
            outputs=[image_edit_components['input_image_info'], image_edit_components['input_image_info']]
        )
        
        image_edit_components['button'].click(
            fn=edit_image,
            inputs=[
                image_edit_components['api_token'],
                image_edit_components['model'],
                image_edit_components['input_image'],
                image_edit_components['prompt'],
                image_edit_components['negative_prompt'],
                image_edit_components['adaptive_ratio'],
                image_edit_components['width'],
                image_edit_components['height'],
                image_edit_components['long_edge'],
                image_edit_components['steps'],
                image_edit_components['guidance'],
                image_edit_components['seed']
            ],
            outputs=[image_edit_components['output_image'], image_edit_components['output_message']]
        )
        
        # 绑定事件 - 文本对话
        text_chat_components['save_token'].change(
            fn=handle_token_save,
            inputs=[text_chat_components['api_token'], text_chat_components['save_token']],
            outputs=[token_status]
        )
        
        text_chat_components['submit_btn'].click(
            fn=chat_with_model,
            inputs=[
                text_chat_components['msg'],
                text_chat_components['chatbot'],
                text_chat_components['api_token'],
                text_chat_components['model'],
                text_chat_components['system_prompt'],
                text_chat_components['max_tokens'],
                text_chat_components['temperature']
            ],
            outputs=[text_chat_components['chatbot'], text_chat_components['msg']]
        )
        
        text_chat_components['msg'].submit(
            fn=chat_with_model,
            inputs=[
                text_chat_components['msg'],
                text_chat_components['chatbot'],
                text_chat_components['api_token'],
                text_chat_components['model'],
                text_chat_components['system_prompt'],
                text_chat_components['max_tokens'],
                text_chat_components['temperature']
            ],
            outputs=[text_chat_components['chatbot'], text_chat_components['msg']]
        )
        
        text_chat_components['clear_btn'].click(
            fn=clear_chat,
            outputs=[text_chat_components['chatbot'], text_chat_components['msg']]
        )
        
        # 绑定事件 - 图生文
        image_to_text_components['save_token'].change(
            fn=handle_token_save,
            inputs=[image_to_text_components['api_token'], image_to_text_components['save_token']],
            outputs=[token_status]
        )
        
        image_to_text_components['input_image'].change(
            fn=update_image_info,
            inputs=[image_to_text_components['input_image']],
            outputs=[image_to_text_components['input_image_info'], image_to_text_components['input_image_info']]
        )
        
        image_to_text_components['button'].click(
            fn=analyze_image_with_text,
            inputs=[
                image_to_text_components['input_image'],
                image_to_text_components['prompt'],
                image_to_text_components['api_token'],
                image_to_text_components['model'],
                image_to_text_components['max_tokens'],
                image_to_text_components['temperature']
            ],
            outputs=[image_to_text_components['output_text']]
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
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False, inbrowser=False)