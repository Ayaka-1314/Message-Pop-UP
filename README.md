# 消息弹窗

一个基于Python的桌面消息弹窗模拟程序，支持多种主题风格和消息类型，提供流畅的动画效果

![Version](https://img.shields.io/badge/version-Beta-yellow?style=flat-square)
![Python](https://img.shields.io/badge/python-3.6+-blue?style=flat-square)
![WeChat](https://img.shields.io/badge/WeChat-停更-red?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2B-lightgrey?style=flat-square)

   
## 功能特点

- 🎨 多主题支持：明亮模式、暗黑模式、黑金模式
- 📱 多应用类型：系统消息、微信、QQ消息模拟
- ✨ 平滑动画：优雅的弹出和消失动画效果
- 🖼️ 自定义图标：支持各主题下的应用图标
- ⚙️ 配置持久化：自动保存主题设置
<img width="585" height="612" alt="image" src="https://github.com/user-attachments/assets/17a2dc58-b9e2-470a-8194-d89dd80787e9" />


## 系统要求

- Python 3.6 或更高版本
- Windows 10/11 或 macOS (Linux可能需额外配置)

## 安装步骤

1. 确保已安装Python环境（可从[Python官网](https://www.python.org/downloads/)下载）
2. 克隆或下载本项目代码
3. 安装所需依赖库：

```bash
pip install pillow
```

注意：Tkinter通常是Python标准库的一部分，但如果遇到问题，可能需要单独安装：
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- CentOS/RHEL: `sudo yum install python3-tk`
- macOS: 预装或使用Homebrew: `brew install python-tk`

## 使用方法

1. 打开命令行/终端，导航到程序所在目录
2. 运行程序：
   ```bash
   python message_popup.py
   ```
3. 在命令行中输入以下命令操作程序：

   - 显示消息：
     ```
     text message    # 系统消息
     text wechat     # 微信消息
     text qq         # QQ消息
     ```

   - 切换主题：
     ```
     theme Light        # 明亮模式
     theme Dark         # 暗黑模式
     theme Black_gold   # 黑金模式
     ```

   - 退出程序：
     ```
     exit
     ```

## 项目结构

```
message_popup.py    # 主程序文件
settings.json       # 自动生成的配置文件(首次运行后创建)
Light/              # 明亮主题图标目录
Dark/               # 暗黑主题图标目录
Black_gold/         # 黑金主题图标目录
```

## 关于微信消息获取的说明

由于微信客户端的持续更新，目前实时监测微信消息的技术方案已失效。微信4.0版本强制升级策略导致无法使用旧版本客户端，而GUI自动化方法又极其复杂且不稳定。

本程序目前仅提供消息弹窗的模拟展示功能，无法直接获取真实微信消息。如果您有微信消息处理的需求，建议：

1. 关注微信官方开放平台可能的API更新
2. 使用企业微信等提供官方接口的替代方案
3. 等待可能的技术突破

如有新的解决方案，我会第一时间更新程序。

## 自定义配置

您可以在各主题目录下自定义图标：
- `message-{主题名}.png` - 系统消息图标
- `wechat-{主题名}.png` - 微信图标
- `qq-{主题名}.png` - QQ图标

推荐图标尺寸：40×40像素，PNG格式带透明通道。

## 常见问题

1. **程序无法启动**
   - 检查Python是否正确安装
   - 确认已安装Pillow库：`pip show pillow`

2. **图标显示不正常**
   - 首次运行会自动生成默认图标
   - 可自定义图标替换自动生成的图标

3. **弹窗位置不正确**
   - 程序会自动适应屏幕尺寸
   - 多显示器环境下可能需要调整代码中的位置计算

## 技术支持

如果您有任何问题或建议，欢迎提出。我会持续关注微信API的变化，一旦有可行的消息获取方案，将立即更新程序，孩纸是一个高中住宿生，解决问题只要在周末能解决哦~

## 赞助孩纸吧
![3fe77d3b879d13b33d68f162b850a2b1](https://github.com/user-attachments/assets/f2f2ad4a-7e85-4e4d-9801-274c9d24c354)
![1b781e0d8d622786b4fa87727f4db6b6](https://github.com/user-attachments/assets/493aa610-0725-46e2-a37b-e2eca7c8542c)
