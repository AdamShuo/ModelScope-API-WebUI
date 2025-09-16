"""
CORS 中间件
用于处理跨域请求和 iframe 嵌入问题
"""

def add_cors_headers(app):
    """为 Gradio 应用添加 CORS 头部"""
    
    @app.middleware("http")
    async def cors_middleware(request, call_next):
        response = await call_next(request)
        
        # 添加 CORS 头部
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
        # 允许 iframe 嵌入
        response.headers["X-Frame-Options"] = "ALLOWALL"
        response.headers["Content-Security-Policy"] = "frame-ancestors *; frame-src *;"
        
        # 其他安全头部
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        
        return response
    
    return app

def setup_cors_for_gradio():
    """为 Gradio 设置跨域支持"""
    import gradio as gr
    
    # 尝试修改 Gradio 的默认配置
    try:
        # 设置允许的源
        if hasattr(gr, 'set_static_paths'):
            gr.set_static_paths(["."])
    except:
        pass
    
    return True