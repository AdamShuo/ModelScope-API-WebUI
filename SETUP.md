# ModelScope API WebUI 安装配置指南

## 🎯 系统要求

### 最低配置
- **操作系统**: Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.15+
- **Python版本**: 3.8 或更高版本
- **内存**: 4GB RAM
- **存储空间**: 至少2GB可用空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **操作系统**: Windows 11, Linux (Ubuntu 20.04+), macOS 12+
- **Python版本**: 3.9 或更高版本
- **内存**: 8GB RAM 或更多
- **存储空间**: 5GB可用空间（用于虚拟环境和依赖包）
- **网络**: 高速互联网连接（用于快速下载依赖）

## 🚀 快速安装

### 方法一：智能启动（推荐）

项目提供智能启动脚本，自动处理所有安装步骤：

#### Windows 用户
1. 下载项目文件到本地
2. 双击运行 `run_windows_smart.bat`
3. 脚本会自动检测环境并完成安装
4. 等待应用启动并在浏览器中打开

#### Linux/macOS 用户
```bash
# 下载项目
git clone https://github.com/AdamShuo/ModelScope-API-WebUI.git
cd ModelScope-API-WebUI

# 赋予执行权限并运行
chmod +x run_linux_smart.sh
./run_linux_smart.sh
```

### 方法二：手动安装

如果需要手动控制安装过程：

```bash
# 克隆项目
git clone https://github.com/AdamShuo/ModelScope-API-WebUI.git
cd ModelScope-API-WebUI

# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动应用
python gradio_app.py
```

### 方法三：无Python环境安装

如果系统没有安装Python，使用独立安装脚本：

#### Windows用户
双击运行 `setup_windows.bat`，或在命令提示符中执行：
```cmd
setup_windows.bat
```

#### Linux/macOS用户
```bash
# 赋予执行权限
chmod +x setup_linux.sh

# 运行安装脚本
./setup_linux.sh
```

安装脚本会：
1. 检测系统Python环境
2. 自动下载安装Python（如果需要）
3. 创建虚拟环境
4. 安装所有依赖包
5. 提供启动指导

## 🔧 详细安装步骤

### Windows 系统安装

#### 1. 环境准备
- 确保系统已安装Python 3.8+
- 如果没有Python，运行 `setup.py` 自动安装

#### 2. 项目设置
```cmd
# 进入项目目录
cd ModelScope-API-WebUI

# 使用智能启动脚本（推荐）
run_windows_smart.bat
```

#### 3. 验证安装
- 控制台显示"应用启动成功"
- 浏览器自动打开 http://127.0.0.1:7860
- 界面正常加载，可输入API Token

### Linux 系统安装

#### 1. 系统依赖
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip
```

#### 2. 项目设置
```bash
# 克隆项目
git clone https://github.com/AdamShuo/ModelScope-API-WebUI.git
cd ModelScope-API-WebUI

# 使用智能启动脚本
chmod +x run_linux_smart.sh
./run_linux_smart.sh
```

### macOS 系统安装

#### 1. 环境准备
```bash
# 使用Homebrew安装Python（如果尚未安装）
brew install python

# 或者从Python官网下载安装包
# https://www.python.org/downloads/macos/
```

#### 2. 项目设置
```bash
# 克隆项目
git clone https://github.com/AdamShuo/ModelScope-API-WebUI.git
cd ModelScope-API-WebUI

# 使用智能启动脚本
chmod +x run_linux_smart.sh
./run_linux_smart.sh
```

## ⚙️ 配置说明

### API Token 配置

首次使用需要配置ModelScope API Token：

1. **获取Token**：
   - 访问 [魔搭社区](https://modelscope.cn) 注册账号
   - 绑定阿里云账号获取免费调用额度
   - 在[访问令牌页面](https://modelscope.cn/my/myaccesstoken)创建令牌

2. **输入Token**：
   - 启动应用后在任意功能模块输入API Token
   - 勾选"保存API Token到浏览器缓存"
   - Token会加密保存在本地

### 模型配置

编辑 `modelscope_config.json` 文件自定义可用模型：

```json
{
  "image_models": ["Qwen/Qwen-Image", "其他模型"],
  "image_edit_models": ["Qwen/Qwen-Image-Edit"],
  "text_models": ["Qwen/Qwen3-Coder-480B-A35B-Instruct"],
  "vision_models": ["stepfun-ai/step3"],
  "default_model": "Qwen/Qwen-Image",
  "timeout": 720,
  "image_download_timeout": 30
}
```

## 🐛 故障排除

### 常见安装问题

#### Python 相关问题

**问题**: "python" 不是内部或外部命令
**解决**: 
- 确保Python已安装并添加到PATH
- 或使用 `setup.py` 自动安装Python

**问题**: 虚拟环境创建失败
**解决**:
- 确保有足够的磁盘空间和权限
- 尝试手动创建：`python -m venv .venv`

#### 依赖安装问题

**问题**: pip安装超时或失败
**解决**:
- 使用国内镜像源：
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

**问题**: 特定包安装失败
**解决**:
- 更新pip：`python -m pip install --upgrade pip`
- 尝试单独安装问题包

#### 启动问题

**问题**: 应用启动后无法访问
**解决**:
- 检查端口7860是否被占用
- 尝试使用其他端口：`python gradio_app.py --port 7861`
- 检查防火墙设置

**问题**: API请求失败
**解决**:
- 确认API Token正确
- 检查网络连接
- 验证每日调用额度

### 平台特定问题

#### Windows 特定问题

**问题**: 批处理脚本无法执行
**解决**:
- 以管理员身份运行命令提示符
- 检查文件路径是否包含中文或特殊字符

**问题**: 权限不足
**解决**:
- 以管理员身份运行脚本
- 检查用户账户控制设置

#### Linux 特定问题

**问题**: 执行权限不足
**解决**:
```bash
chmod +x *.sh
chmod +x *.py
```

**问题**: 依赖库缺失
**解决**:
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

#### macOS 特定问题

**问题**: SSL证书错误
**解决**:
```bash
# 安装Certificates
pip install certifi
/Applications/Python\ 3.*/Install\ Certificates.command
```

**问题**: 架构兼容性问题
**解决**:
- 确保使用对应架构的Python（Intel/Apple Silicon）

## 🔒 安全配置

### 文件权限设置

确保敏感文件有适当权限：
```bash
# Linux/macOS
chmod 600 .api_token .token_key
chmod 700 .venv

# Windows
icacls .api_token /inheritance:r /grant:r "%username%:F"
icacls .token_key /inheritance:r /grant:r "%username%:F"
```

### 网络安全

- 应用默认只在本地访问（127.0.0.1）
- 如需远程访问，配置适当的防火墙规则
- 不要将应用暴露在公共网络 without 适当认证

## 📊 性能优化

### 虚拟环境优化

```bash
# 清理缓存
pip cache purge

# 优化虚拟环境大小
# 删除不必要的包和缓存
```

### 启动优化

- 使用快速启动脚本（如果虚拟环境已存在）
- 关闭不必要的后台应用释放内存
- 确保有足够的可用内存

### 网络优化

- 使用稳定的网络连接
- 避免在网络高峰期进行大量API调用
- 考虑使用本地代理改善连接稳定性

## 🔄 更新与维护

### 项目更新

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 重启应用
```

### 环境维护

定期清理：
```bash
# 清理pip缓存
pip cache purge

# 检查虚拟环境大小
du -sh .venv

# 更新所有包
pip list --outdated
pip install --upgrade $(pip list --outdated | awk 'NR>2 {print $1}')
```

### 数据备份

重要文件备份：
- `.api_token` - API Token加密文件
- `.token_key` - 加密密钥文件
- 自定义的模型配置文件
- 保存的参数模板文件

## 🤝 获取帮助

如果遇到无法解决的问题：

1. **查看日志**：控制台输出详细的错误信息
2. **检查文档**：README.md 和 USAGE.md 包含详细说明
3. **社区支持**：在GitHub Issues中提出问题
4. **版本检查**：确保使用最新版本的应用

---

**提示**: 本安装指南会随版本更新而调整，建议定期查看最新版本以获取最新安装信息。