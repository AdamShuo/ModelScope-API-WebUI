"""
Photopea模块
处理在线图像编辑器的嵌入功能
"""

import gradio as gr

# Handy constants
PHOTOPEA_MAIN_URL = "https://www.photopea.com/"
PHOTOPEA_IFRAME_ID = "webui-photopea-iframe"
PHOTOPEA_IFRAME_HEIGHT = 768
PHOTOPEA_IFRAME_WIDTH = "100%"
PHOTOPEA_IFRAME_LOADED_EVENT = "onPhotopeaLoaded"

def create_photopea_collapsible_component():
    """创建可折叠的底部Photopea组件"""
    with gr.Column():
        gr.Markdown("---")  # 分隔线
        
        with gr.Accordion("🎨 Photopea 在线图像编辑器 (点击展开/折叠)", open=False):
            gr.Markdown("""
            ### 📝 使用说明
            **功能强大的在线图像编辑器，类似于 Photoshop，支持多种图像格式。**
            
            💡 **提示：** 您可以直接拖拽图片到下方编辑器中开始编辑，编辑状态在所有标签间保持不变。
            """)
            
            with gr.Row():
                # 嵌入 Photopea 网站
                gr.HTML(f"""<iframe id="{PHOTOPEA_IFRAME_ID}" 
                    src = "{PHOTOPEA_MAIN_URL}{get_photopea_url_params()}" 
                    width = "{PHOTOPEA_IFRAME_WIDTH}" 
                    height = "{PHOTOPEA_IFRAME_HEIGHT}"
                    onload = "{PHOTOPEA_IFRAME_LOADED_EVENT}(this)"
                    style="border: 1px solid #ddd; border-radius: 8px;">
                </iframe>""")
            
            with gr.Row():
                gr.Markdown("""
                ### 使用提示：
                - 🎨 支持 PSD、XCF、Sketch 等多种格式
                - 📁 可以直接拖拽图片到编辑器中
                - 🔧 提供图层、滤镜、画笔等专业工具
                - 💾 编辑完成后可导出为各种格式
                - 🆓 完全免费使用，无需注册
                - ✨ **编辑状态在所有标签中保持，切换标签不会丢失进度**
                
                **注意：** 如果编辑器无法正常加载，可能是网络问题或浏览器安全设置导致。您可以直接访问 [www.photopea.com](https://www.photopea.com) 使用。
                """)
            
        # Initialize Photopea with an empty, 512x512 white image. It's baked as a base64 string with URI encoding.
def get_photopea_url_params():
    return "#%7B%22resources%22:%5B%22data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIAAQMAAADOtka5AAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAANQTFRF////p8QbyAAAADZJREFUeJztwQEBAAAAgiD/r25IQAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfBuCAAAB0niJ8AAAAABJRU5ErkJggg==%22%5D%7D"