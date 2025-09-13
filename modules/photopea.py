"""
Photopea模块
处理在线图像编辑器的嵌入功能
"""

import gradio as gr

def create_photopea_interface():
    """创建Photopea标签页界面"""
    with gr.Tab("Photopea"):
        gr.Markdown("## 在线图像编辑器 - Photopea")
        gr.Markdown("Photopea 是一个功能强大的在线图像编辑器，类似于 Photoshop，支持多种图像格式。您可以直接拖拽图片到编辑器中开始编辑。")
        
        # 嵌入 Photopea 网站
        gr.HTML("""
        <iframe 
            src="https://www.photopea.com" 
            width="100%" 
            height="800px" 
            frameborder="0" 
            style="border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        </iframe>
        """)
        
        gr.Markdown("""
        ### 使用提示：
        - 🎨 支持 PSD、XCF、Sketch 等多种格式
        - 📁 可以直接拖拽图片到编辑器中
        - 🔧 提供图层、滤镜、画笔等专业工具
        - 💾 编辑完成后可导出为各种格式
        - 🆓 完全免费使用，无需注册
        
        **注意：** 如果上方编辑器无法正常加载，可能是网络问题或浏览器安全设置导致。您可以直接访问 [www.photopea.com](https://www.photopea.com) 使用。
        """)