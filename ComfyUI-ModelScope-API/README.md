# ModelScope API WebUI

基于ModelScope API的现代化Web应用，提供完整的AI模型服务访问界面。

## ✨ 功能特性

- **🎨 文生图**：输入文本描述生成高质量图像
- **✏️ 图像编辑**：基于原图进行AI驱动的图像编辑和修改
- **💬 文本对话**：支持多轮对话的智能聊天功能
- **🔍 图生文**：图像描述和视觉问答功能
- **🌐 现代化界面**：基于Gradio构建的直观Web界面
- **⚙️ 灵活配置**：支持模型切换、参数调节和API Token缓存
- **📱 响应式设计**：支持桌面和移动设备访问

## 🚀 快速开始

### 环境要求

- Python 3.8+
- ModelScope API Token

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/AdamShuo/ModelScope-API-WebUI.git
cd ModelScope-API-WebUI

# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

**依赖说明：**
- 所有必需的依赖包都列在 `requirements.txt` 文件中
- 包含核心功能所需的基础库和可选的增强功能库
- 建议使用虚拟环境以避免包冲突

### 启动应用

```bash
python gradio_app.py
```

应用将在 http://localhost:7860 启动，支持局域网访问。

## 🎯 功能模块

### 1. 文生图 (Text-to-Image)
- 支持多种AI图像生成模型
- 可调节图像尺寸（最高2048px）
- 支持正面和负面提示词
- 可控制采样步数、引导系数和随机种子

### 2. 图像编辑 (Image Editing)
- 上传原图进行AI编辑
- 自适应原图比例功能
- 支持风格转换和内容修改
- 实时显示输入图像尺寸信息

### 3. 文本对话 (Text Chat)
- 多轮对话支持
- 可自定义系统提示词
- 支持多种大语言模型
- 可调节温度和最大Token数

### 4. 图生文 (Image-to-Text)
- 图像内容描述
- 视觉问答功能
- 支持自定义分析提示词
- 多语言输出支持

## ⚙️ 配置说明

### API Token设置

1. 在任意功能模块中输入您的ModelScope API Token
2. 勾选"保存API Token到浏览器缓存"以便下次自动加载
3. Token将安全保存在浏览器本地存储中

### 模型配置

编辑 `modelscope_config.json` 文件来自定义可用模型列表：

```json
{
  "image_models": ["Qwen/Qwen-Image", "其他图像模型"],
  "image_edit_models": ["Qwen/Qwen-Image-Edit"],
  "text_models": ["Qwen/Qwen3-Coder-480B-A35B-Instruct"],
  "vision_models": ["stepfun-ai/step3"],
  "default_model": "Qwen/Qwen-Image",
  "timeout": 720,
  "image_download_timeout": 30
}
```

### 参数说明

| 参数 | 范围 | 说明 |
|------|------|------|
| 图像尺寸 | 256-2048px | 生成图像的宽度和高度 |
| 采样步数 | 1-100 | 影响图像质量和生成时间 |
| 引导系数 | 1.0-20.0 | 控制提示词的影响强度 |
| 随机种子 | -1或正整数 | -1为随机，固定值可复现结果 |
| 温度 | 0.1-2.0 | 文本生成的随机性程度 |
| 最大Token | 100-8000 | 文本生成的最大长度 |

## 🔧 技术架构

- **前端框架**：Gradio
- **后端API**：ModelScope API
- **图像处理**：PIL (Pillow)
- **HTTP客户端**：Requests
- **AI模型接口**：OpenAI兼容接口

## 📦 项目结构

```
ModelScope-API-WebUI/
├── gradio_app.py              # 主应用文件
├── modelscope_config.json     # 模型配置文件
├── requirements.txt           # 依赖包列表
├── README.md                  # 项目说明
├── .gitignore                # Git忽略文件
└── .venv/                    # 虚拟环境（本地）
```

## 🛠️ 开发指南

### 添加新模型

1. 在 `modelscope_config.json` 中添加模型名称
2. 重启应用即可在界面中看到新模型

### 自定义界面

修改 `gradio_app.py` 中的界面组件和布局来自定义用户界面。

### API集成

项目使用ModelScope API，支持异步任务处理和状态轮询。

## 🔍 故障排除

### 常见问题

1. **API请求失败**：检查API Token是否正确，网络连接是否正常
2. **模型不可用**：某些模型可能需要特定权限或处于维护状态
3. **图像生成超时**：可以在配置文件中调整timeout参数
4. **依赖安装失败**：确保Python版本>=3.8，使用虚拟环境

### 日志查看

应用运行时会在控制台输出详细的处理日志，包括：
- API请求状态
- 任务ID和进度
- 错误信息和调试信息

## 🔒 安全注意事项

### API Token 保护

本应用会将API Token加密保存在本地文件中，生成以下文件：
- `.api_token` - 加密的API Token文件
- `.token_key` - 加密密钥文件

**⚠️ 重要安全提醒：**

在以下情况下，请务必手动删除这两个文件：
1. **项目迁移**：将项目复制到其他机器或位置时
2. **代码分享**：上传到Git仓库或分享给他人时
3. **系统重装**：重装系统或更换设备时
4. **不再使用**：停止使用本应用时

**删除命令：**
```bash
# Linux/Mac
rm .api_token .token_key

# Windows
del .api_token .token_key
```

**为什么需要删除：**
- 防止API Token泄露给未授权用户
- 避免在不同环境间意外共享敏感信息
- 确保每个环境使用独立的加密密钥

这些文件已自动添加到 `.gitignore` 中，正常情况下不会被Git跟踪。

## 🙏 致谢

本项目基于 [ComfyUI-ModelScope-API](https://github.com/hujuying/ComfyUI-ModelScope-API) 项目进行开发和改进。

感谢原项目作者 [@hujuying](https://github.com/hujuying) 提供的优秀基础代码和创意思路，为ModelScope API的集成提供了宝贵的参考。本项目在原有基础上进行了重构，转换为独立的Gradio WebUI应用，并添加了更多功能特性。

## 📄 许可证

MIT License

Copyright (c) 2024 ModelScope API WebUI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

在贡献代码前，请确保：
- 遵循现有的代码风格
- 添加适当的注释和文档
- 测试新功能的稳定性

## 📞 支持

如有问题，请在GitHub Issues中提出。

我们会尽快回复并提供帮助。