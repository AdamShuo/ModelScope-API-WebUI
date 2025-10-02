# ModelScope API WebUI

基于ModelScope API的现代化Web应用，提供完整的AI模型服务访问界面。

## ✨ 功能特性

- **🎨 文生图**：输入文本描述生成高质量图像，支持元数据嵌入
- **✏️ 图像编辑**：基于原图进行AI驱动的图像编辑和修改，支持参数保存
- **💬 文本对话**：支持多轮对话的智能聊天功能
- **🔍 图生文**：图像描述和视觉问答功能
- **🖼️ Photopea**：内嵌在线图像编辑器，类似Photoshop的专业编辑功能
- **✍️ 手绘白板**：集成 Excalidraw 和 tldraw 两款专业手绘白板工具
- **🌐 现代化界面**：基于Gradio构建的直观Web界面
- **⚙️ 灵活配置**：支持模型切换、参数调节和API Token缓存
- **📱 响应式设计**：支持桌面和移动设备访问
- **🔧 模块化架构**：代码结构清晰，便于维护和扩展
- **📊 元数据管理**：生成的图像自动包含完整生成参数
- **💾 参数保存/加载**：支持参数保存为JSON文件和从图像/文件加载参数
- **🔄 参数复用**：可重复使用保存的参数进行批量处理

## 🚀 快速开始

### 环境要求

- Python 3.8+
- ModelScope API Token（免费获取，详见下方说明）

### 🔑 获取 ModelScope API Token

使用本应用需要先获取ModelScope API Token，完全免费且提供每日2000次调用额度：

#### 📋 获取步骤

1. **注册魔搭账号**
   - 访问 [魔搭社区](https://modelscope.cn)
   - 点击右上角"登录/注册"
   - 使用手机号或邮箱完成注册

2. **绑定阿里云账号**
   - 登录魔搭账号后，进入个人中心
   - 按提示绑定阿里云账号（如无阿里云账号需先注册）
   - 绑定成功后即可获得每日2000次免费调用额度

3. **创建访问令牌**
   - 访问 [访问令牌页面](https://modelscope.cn/my/myaccesstoken)
   - 点击"新建令牌"
   - 设置令牌名称（如：WebUI-Token）
   - 复制生成的访问令牌

4. **在应用中使用**
   - 启动本应用后，在任意功能模块中粘贴API Token
   - 勾选"保存API Token到浏览器缓存"以便下次自动加载
   - 开始使用各项AI功能

#### 💡 使用提示

- **免费额度**：每日2000次调用，足够个人使用
- **重置时间**：每日0点重置调用次数
- **Token安全**：请妥善保管您的API Token，不要分享给他人
- **多设备使用**：同一Token可在多个设备上使用

### 🎯 一键启动（推荐）

项目提供智能启动脚本，自动检测Python环境并选择最佳启动方式：

#### 🧠 智能启动
智能检测Python环境，自动选择最佳启动方式：

##### Windows 用户
双击运行 `run_windows_smart.bat`

##### Linux/macOS 用户
```bash
chmod +x run_linux_smart.sh
./run_linux_smart.sh
```

#### 🌟 脚本特性
- ✅ **智能环境检测**：自动检测Python可用性，优先使用虚拟环境Python
- ✅ **跨平台兼容**：支持Windows、Linux、macOS系统
- ✅ **无Python支持**：即使没有系统Python也能运行
- ✅ **自动环境管理**：自动创建和激活虚拟环境
- ✅ **依赖自动安装**：自动安装所需依赖包
- ✅ **深色主题**：自动使用深色主题启动
- ✅ **智能等待**：等待8秒确保应用完全启动
- ✅ **自动打开浏览器**：无需手动输入地址
- ✅ **中英文提示**：友好的双语操作提示
- ✅ **安全退出**：按指定键安全停止应用
- ✅ **环境隔离**：强制使用虚拟环境Python，防止污染系统环境

### 手动安装（可选）

如果需要手动配置环境：

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

# 启动应用
python gradio_app.py
```

### 🔧 环境设置脚本

项目提供了独立安装脚本，适应不同操作系统：

#### Windows 用户
双击运行 `setup_windows.bat`

#### Linux/macOS 用户
```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

这些脚本会：
- 自动检测操作系统类型
- 下载并安装Python（如果需要）
- 创建虚拟环境
- 安装所有依赖包
- 提供启动指导

### 🌐 访问地址

- **本地访问**: http://127.0.0.1:7860
- **深色主题**: http://127.0.0.1:7860/?__theme=dark（脚本默认）
- **浅色主题**: http://127.0.0.1:7860/?__theme=light

## 🎯 功能模块

### 1. 文生图 (Text-to-Image)
- 支持多种AI图像生成模型
- 可调节图像尺寸（最高2048px）
- 支持正面和负面提示词
- 可控制采样步数、引导系数和随机种子
- **元数据嵌入**：生成的图像自动包含完整生成参数（可选）
- **参数管理**：支持保存/加载生成参数为JSON文件
- **参数复用**：可从包含元数据的图像自动加载参数

### 2. 图像编辑 (Image Editing)
- 上传原图进行AI编辑
- 自适应原图比例功能
- 支持风格转换和内容修改
- 实时显示输入图像尺寸信息
- **元数据嵌入**：编辑后的图像包含原图和编辑参数（可选）
- **参数管理**：支持保存/加载编辑参数为JSON文件
- **参数继承**：可从原图自动继承生成参数

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

### 5. Photopea 在线编辑器
- 内嵌专业级在线图像编辑器
- 支持 PSD、XCF、Sketch 等多种格式
- 提供图层、滤镜、画笔等专业工具
- 无需安装，直接在浏览器中使用
- 完全免费，功能媲美 Photoshop

### 6. 手绘白板
- **Excalidraw**：简洁优雅的手绘风格白板，支持图形绘制、文本标注
- **tldraw**：功能丰富的现代化白板工具，支持多种绘图模式
- **状态保持**：两个白板工具独立运行，切换时保持各自的编辑状态
- **实时协作**：支持多人实时协作编辑（需要相应服务支持）
- **导出功能**：支持导出为 PNG、SVG 等多种格式

## ⚙️ 配置说明

### API Token设置

1. **获取Token**：按照上方"🔑 获取 ModelScope API Token"步骤获取您的访问令牌
2. **输入Token**：在任意功能模块中粘贴您的ModelScope API Token
3. **保存设置**：勾选"保存API Token到浏览器缓存"以便下次自动加载
4. **安全存储**：Token将加密保存在本地，确保使用安全

💡 **首次使用提示**：
- 确保已完成魔搭账号注册和阿里云账号绑定
- 每日有2000次免费调用额度，足够个人使用
- Token输入一次后会自动保存，无需重复输入

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
- **模块化设计**：功能模块独立，便于维护和扩展
- **加密存储**：API Token 本地加密保存
- **元数据管理**：EXIF标准元数据嵌入和提取
- **参数序列化**：JSON格式参数保存和加载
- **文件操作**：安全的临时文件管理和标准对话框

## 📦 项目结构

```
ModelScope-API-WebUI/
├── gradio_app.py              # 主应用文件（模块化重构版）
├── modules/                   # 功能模块文件夹
│   ├── __init__.py           # 模块包初始化
│   ├── common.py             # 公共函数和工具
│   ├── text_to_image.py      # 文生图模块
│   ├── image_edit.py         # 图像编辑模块
│   ├── text_chat.py          # 文本对话模块
│   ├── image_to_text.py      # 图生文模块
│   ├── photopea.py           # Photopea在线编辑器模块
│   └── whiteboard.py         # 手绘白板模块
├── modelscope_config.json     # 模型配置文件
├── requirements.txt           # 依赖包列表
├── README.md                  # 项目说明
├── 运行说明.md                # 详细运行说明
├── run_windows_smart.bat      # Windows智能启动脚本
├── run_linux_smart.sh         # Linux/macOS智能启动脚本
├── setup.py                   # 跨平台安装脚本
├── .gitignore                # Git忽略文件
└── .venv/                    # 虚拟环境（本地）
```

### 🏗️ 模块化架构说明

项目采用模块化设计，将不同功能分离到独立的模块中：

- **`gradio_app.py`**：主应用文件，负责界面组装和事件绑定
- **`modules/common.py`**：公共功能模块，包含API Token管理、配置加载、图像处理等
- **`modules/text_to_image.py`**：文生图功能的完整实现
- **`modules/image_edit.py`**：图像编辑功能的完整实现
- **`modules/text_chat.py`**：文本对话功能的完整实现
- **`modules/image_to_text.py`**：图生文功能的完整实现
- **`modules/photopea.py`**：Photopea在线编辑器的界面实现
- **`modules/whiteboard.py`**：手绘白板功能，集成 Excalidraw 和 tldraw

#### 🎯 模块化优势

1. **代码组织清晰**：每个功能模块独立管理，职责单一
2. **便于维护**：修改特定功能时只需编辑对应模块
3. **易于扩展**：添加新功能只需创建新模块并在主文件中引用
4. **降低耦合**：模块间依赖关系清晰，减少代码耦合
5. **提高可读性**：主文件从近1000行缩减到约400行

## 🛠️ 开发指南

### 添加新模型

1. 在 `modelscope_config.json` 中添加模型名称
2. 重启应用即可在界面中看到新模型

### 添加新功能模块

1. **创建模块文件**：在 `modules/` 文件夹中创建新的 `.py` 文件
2. **实现功能函数**：编写具体的功能实现代码
3. **创建界面函数**：编写 Gradio 界面创建函数
4. **主文件集成**：在 `gradio_app.py` 中导入并使用新模块

#### 示例：添加新模块

```python
# modules/new_feature.py
def new_feature_function(param1, param2):
    """新功能的实现"""
    # 功能实现代码
    return result

def create_new_feature_interface():
    """创建新功能的界面"""
    with gr.Tab("新功能"):
        # 界面组件定义
        pass
```

```python
# gradio_app.py 中添加导入和使用
from modules.new_feature import new_feature_function, create_new_feature_interface

# 在 create_gradio_interface() 中调用
create_new_feature_interface()
```

### 修改现有功能

1. **定位模块**：找到对应功能的模块文件
2. **修改实现**：直接在模块文件中修改功能实现
3. **测试验证**：重启应用测试修改效果

### 自定义界面

- **主界面布局**：修改 `gradio_app.py` 中的界面组装逻辑
- **单个模块界面**：修改对应模块文件中的界面创建函数
- **公共组件**：在 `modules/common.py` 中添加可复用的界面组件

### API集成

项目使用ModelScope API，支持异步任务处理和状态轮询。相关功能主要在以下模块中：

- **API请求**：`modules/common.py` 中的 `make_api_request_with_retry()`
- **文生图API**：`modules/text_to_image.py`
- **图像编辑API**：`modules/image_edit.py`
- **对话API**：`modules/text_chat.py`
- **视觉API**：`modules/image_to_text.py`

### 代码规范

1. **模块职责单一**：每个模块只负责一个主要功能
2. **函数命名清晰**：使用描述性的函数名
3. **添加文档字符串**：为函数和模块添加说明文档
4. **错误处理**：适当添加异常处理和用户友好的错误信息
5. **导入规范**：相对导入模块内部依赖，绝对导入外部依赖

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