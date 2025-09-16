"""
手绘白板模块
处理 Excalidraw 和 tldraw 在线白板工具的嵌入功能
"""

import gradio as gr

# 白板工具常量
EXCALIDRAW_URL = "https://excalidraw.com/"
TLDRAW_URL = "https://www.tldraw.com/"
IFRAME_HEIGHT = 700
IFRAME_WIDTH = "100%"

def create_whiteboard_tab(config, saved_token):
    """创建手绘白板标签页"""
    with gr.Tab("手绘白板"):
        with gr.Row():
            with gr.Column(scale=1):
                # 白板工具选择
                whiteboard_tool = gr.Radio(
                    label="选择白板工具",
                    choices=["Excalidraw", "tldraw"],
                    value="Excalidraw",
                    info="选择您想要使用的手绘白板工具"
                )
                
                gr.Markdown("""
                ### 🎨 白板工具说明
                
                **Excalidraw：**
                - 手绘风格的图表和草图工具
                - 支持多种形状、箭头、文字
                - 简洁直观的界面设计
                - 适合制作流程图、思维导图
                
                **tldraw：**
                - 现代化的绘图和白板工具
                - 支持自由绘制和几何图形
                - 强大的协作功能
                - 适合创意设计和原型制作
                
                ### 💡 使用提示
                - 选择上方的工具后，右侧会显示对应的白板
                - 两个工具的编辑状态独立保存
                - 可以随时切换工具而不丢失内容
                """)
            
            with gr.Column(scale=2):
                # Excalidraw iframe
                excalidraw_frame = gr.HTML(
                    value=f"""<iframe 
                        src="{EXCALIDRAW_URL}" 
                        width="{IFRAME_WIDTH}" 
                        height="{IFRAME_HEIGHT}"
                        frameborder="0"
                        style="border: 1px solid #ddd; border-radius: 8px;">
                    </iframe>""",
                    visible=True,
                    label="Excalidraw 白板"
                )
                
                # tldraw iframe
                tldraw_frame = gr.HTML(
                    value=f"""<iframe 
                        src="{TLDRAW_URL}" 
                        width="{IFRAME_WIDTH}" 
                        height="{IFRAME_HEIGHT}"
                        frameborder="0"
                        style="border: 1px solid #ddd; border-radius: 8px;">
                    </iframe>""",
                    visible=False,
                    label="tldraw 白板"
                )
        
        return {
            'whiteboard_tool': whiteboard_tool,
            'excalidraw_frame': excalidraw_frame,
            'tldraw_frame': tldraw_frame
        }

def switch_whiteboard_tool(tool_choice):
    """切换白板工具显示"""
    if tool_choice == "Excalidraw":
        return gr.update(visible=True), gr.update(visible=False)
    else:  # tldraw
        return gr.update(visible=False), gr.update(visible=True)