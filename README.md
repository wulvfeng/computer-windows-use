# Computer MCP

> 基于 Model Context Protocol 的 Windows 电脑操控服务器

让支持 MCP 的大模型（如 Claude、GPT-4o、Cursor、Codex 等）通过标准 MCP 协议操控你的 Windows 电脑。

**本项目是 MCP Server，不是 Agent。** 它只提供能力（Tools/Resources/Prompts），由外部模型决定如何使用。

## 功能特性

- **屏幕观测**: 截图、区域截图、多显示器支持、DPI 自适应
- **鼠标控制**: 移动、点击、双击、右键、拖拽、滚轮，支持拟人化轨迹
- **键盘输入**: 文本输入通过剪贴板粘贴，兼容中英文输入法（IME），不会触发候选词
- **键盘控制**: 按键、组合键（Enter、Tab、Ctrl+C 等），直接模拟按键事件
- **窗口管理**: 窗口枚举、聚焦、位置查询
- **系统信息**: 进程查询、CPU/内存/磁盘使用率、服务健康检查
- **AI 操控浮窗**: 操控时顶部显示状态提示，支持自定义 AI 名称
- **安全机制**: 危险快捷键拦截、操作次数限制、日志审计、紧急停止
- **坐标系统**: 绝对坐标 + 归一化坐标，DPI 感知，适配多显示器

## 架构

```
┌──────────────────────────────────────────────────────┐
│                    MCP Clients                        │
│              (Claude / GPT-4o / Cursor)               │
└────────────────────────┬─────────────────────────────┘
                         │ MCP Protocol (stdio / SSE)
┌────────────────────────▼─────────────────────────────┐
│                  MCP Layer (mcp_server/)              │
│         server.py · tool_registry · prompts           │
├──────────────────────────────────────────────────────┤
│                  Tool Layer (tools/*/tool.py)         │
│            参数解析 · MCP 工具函数定义                   │
├──────────────────────────────────────────────────────┤
│                Service Layer (services/)              │
│          业务逻辑 · 坐标转换 · 安全校验                  │
├──────────────────────────────────────────────────────┤
│               Driver Layer (tools/*/driver.py)        │
│         pynput · human-mouse · humandriver            │
│         mss · pywin32 · psutil                        │
└──────────────────────────────────────────────────────┘
```

### 设计原则

1. **MCP 层**只负责暴露工具
2. **Tool 层**只负责参数解析
3. **Service 层**负责业务逻辑
4. **Driver 层**负责调用第三方库
5. 所有第三方库被封装，支持替换底层实现
6. 所有代码均有类型注解

## 安装

### 环境要求

- Windows 10 / Windows 11
- Python 3.11+

### 安装依赖

```bash
# 方式一：pip install（推荐，支持 editable 安装）
pip install -e .

# 方式二：requirements.txt
pip install -r requirements.txt

# 带可选功能
pip install -e ".[human]"      # 拟人化驱动
```

### 从源码安装

```bash
git clone https://github.com/your-username/computer-mcp.git
cd computer-mcp
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[human]"
```

## 配置

### 快速开始（无需配置）

**默认配置即可直接运行**，所有配置项都有合理的默认值。如果你只是想试试，直接跳到「使用」章节。

### `.env` 文件配置

如需自定义配置，在项目根目录创建 `.env` 文件：

```powershell
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

[.env.example](file:///e:/Desktop/GitHub/windows-computer-use-vllm/computer-mcp/.env.example) 包含所有配置项及详细中文注释，按需修改即可。

### 环境变量

所有配置项均以 `COMPUTER_MCP_` 为前缀，支持 `.env` 文件和系统环境变量（环境变量优先级更高）。

### 配置项一览

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `COMPUTER_MCP_TRANSPORT` | `stdio` | 传输方式：`stdio` / `sse` |
| `COMPUTER_MCP_MOUSE_DRIVER` | `pynput` | 鼠标驱动：`pynput` / `human_mouse` |
| `COMPUTER_MCP_KEYBOARD_DRIVER` | `pynput` | 键盘驱动：`pynput` / `humandriver` |
| `COMPUTER_MCP_AI_ASSISTANT_NAME` | `AI` | AI 助手名称（浮窗显示） |
| `COMPUTER_MCP_SAFE_MODE` | `true` | 安全模式开关 |
| `COMPUTER_MCP_MAX_ACTIONS_PER_SESSION` | `200` | 单次会话最大操作次数 |
| `COMPUTER_MCP_LOG_LEVEL` | `INFO` | 日志级别 |
| `COMPUTER_MCP_SCREENSHOT_MAX_WIDTH` | `1920` | 截图最大宽度 |

> 完整配置项请参考 [.env.example](file:///e:/Desktop/GitHub/windows-computer-use-vllm/computer-mcp/.env.example)（包含每个选项的详细注释）。

## 使用

### 启动服务

```bash
# stdio 模式（默认，推荐）
python main.py

# SSE 模式
COMPUTER_MCP_TRANSPORT=sse python main.py
```

### MCP 客户端配置

#### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "computer": {
      "command": "python",
      "args": ["E:\\path\\to\\computer-mcp\\main.py"]
    }
  }
}
```

#### Cursor (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "computer": {
      "command": "python",
      "args": ["E:\\path\\to\\computer-mcp\\main.py"]
    }
  }
}
```

#### Claude Code

```bash
claude mcp add computer python E:\\path\\to\\computer-mcp\\main.py
```

## MCP 工具列表

共 **23 个**工具，分为 5 大类。

### Screen（屏幕）

| 工具 | 说明 |
|------|------|
| `get_screen_info` | 获取所有显示器信息（分辨率、DPI、位置） |
| `take_screenshot` | 截取全屏，保存到文件并返回路径 |
| `take_region_screenshot` | 截取指定区域 |
| `get_mouse_position` | 获取当前鼠标位置 |
| `observe` | **一次性获取完整电脑状态**（屏幕 + 鼠标 + 窗口） |

### Mouse（鼠标）

| 工具 | 说明 |
|------|------|
| `move_mouse` | 移动鼠标到指定位置 |
| `click` | 点击（支持按钮、次数） |
| `double_click` | 双击 |
| `right_click` | 右键点击 |
| `drag` | 从 A 点拖拽到 B 点 |
| `scroll` | 滚轮滚动 |

### Keyboard — 文本输入

| 工具 | 说明 |
|------|------|
| `type_text` | 输入文本（通过剪贴板粘贴，兼容中英文输入法） |

### Keyboard — 键盘控制

| 工具 | 说明 |
|------|------|
| `press_key` | 按下并释放一个键（Enter、Tab、Escape 等） |
| `key_down` | 按下按键（不释放） |
| `key_up` | 释放按键 |
| `hotkey` | 组合键（如 Ctrl+C、Alt+Tab） |

### Window（窗口）

| 工具 | 说明 |
|------|------|
| `list_windows` | 列出所有可见窗口 |
| `active_window` | 获取当前活动窗口 |
| `focus_window` | 聚焦指定窗口（按标题或句柄） |
| `window_rect` | 获取窗口位置和大小 |

### System（系统）

| 工具 | 说明 |
|------|------|
| `sleep` | 等待指定时间 |
| `ping` | 检查服务状态 |
| `list_processes` | 列出运行中的进程（名称、PID、CPU、内存） |
| `find_process` | 查找某个应用是否在运行 |
| `get_system_stats` | 获取 CPU/内存/磁盘使用率 |

## AI 操控浮窗

当 AI 通过 MCP 操控电脑时，屏幕顶部会显示一个半透明浮窗：

```
● Claude 正在操控您的电脑
● Claude 正在操控: click
● Claude 正在操控: type_text
```

- 操作时实时更新操作名称
- 5 秒无操作自动隐藏
- 名称通过 `COMPUTER_MCP_AI_ASSISTANT_NAME` 配置

## 坐标系统

支持两种坐标模式，已适配 DPI 缩放和多显示器：

### 绝对坐标

```json
{"x": 1000, "y": 500}
```

### 归一化坐标

```json
{"x": 0.5, "y": 0.4, "normalized": true}
```

归一化坐标 (0.0~1.0) 基于主显示器分辨率转换，适用于不同 DPI 和分辨率。

### 多显示器

- `monitor_index=0` 表示虚拟屏幕（所有显示器合并）
- `monitor_index=1,2,...` 表示单个显示器
- 归一化坐标基于主显示器尺寸计算

## 日志系统

日志保存在 `logs/` 目录下：

| 文件 | 说明 |
|------|------|
| `computer_mcp.log` | 全量日志（DEBUG 及以上），按 10MB 轮转，保留 7 天 |
| `crash.log` | 崩溃日志（ERROR 及以上），带完整堆栈，保留 30 天 |
| `audit.log` | 操作审计日志，记录所有 MCP 工具调用 |

调试时查看 `logs/crash.log` 可快速定位崩溃原因。

## MCP Prompts

| 提示词 | 说明 |
|--------|------|
| `computer_use_guide` | 电脑操作完整指南 |
| `observe_and_act(task)` | 引导模型观察并执行指定任务 |
| `debugging_guide` | 操作失败调试指南 |

## MCP Resources

| 资源 URI | 说明 |
|----------|------|
| `computer-mcp://config` | 服务配置信息（脱敏） |
| `computer-mcp://keys` | 支持的按键名称列表 |

## 安全机制

### Safe Mode（安全模式）

默认开启，提供以下保护：

- **危险快捷键拦截**: Alt+F4、Ctrl+Shift+Delete、Win+L 等
- **操作次数限制**: 单次会话最多 200 次操作（可配置）
- **坐标边界校验**: 阻止超出屏幕范围的操作
- **紧急停止**: 通过 F12 触发紧急停止
- **日志审计**: 所有操作记录到审计日志

### 危险快捷键黑名单

```
alt+f4, ctrl+shift+delete, ctrl+alt+delete, win+l, win+u
```

可通过配置文件自定义扩展。

## 项目结构

```
computer-mcp/
├── main.py                  # MCP 入口
├── pyproject.toml           # 项目配置与依赖
├── requirements.txt         # 依赖清单（pip install -r 方式）
├── .env.example             # 环境变量配置示例
├── .env                     # 本地配置（不提交到 Git）
├── config/                  # 配置层
│   ├── settings.py          # 全局配置（pydantic-settings）
│   ├── constants.py         # 常量定义（键名映射、DPI 表）
│   └── logging.py           # loguru 日志配置
├── core/                    # 核心层
│   ├── exceptions.py        # 分层异常体系
│   ├── result.py            # 统一结果类型 ToolResult
│   ├── security.py          # 安全守卫 SecurityGuard
│   ├── overlay.py           # AI 操控浮窗
│   └── base_tool.py         # 工具协议定义
├── schemas/                 # 数据模型层
│   ├── screen.py            # 屏幕/坐标/截图模型
│   ├── mouse.py             # 鼠标操作参数模型
│   ├── keyboard.py          # 键盘操作参数模型
│   ├── window.py            # 窗口信息模型
│   └── system.py            # 系统信息模型
├── services/                # 服务层（业务逻辑）
│   ├── screen_service.py    # 屏幕服务
│   ├── mouse_service.py     # 鼠标服务
│   ├── keyboard_service.py  # 键盘服务
│   ├── window_service.py    # 窗口服务
│   └── system_service.py    # 系统服务
├── tools/                   # 驱动层 + 工具注册
│   ├── screen/              # 截图驱动 + 显示器信息
│   ├── mouse/               # 鼠标驱动（pynput / human-mouse）
│   ├── keyboard/            # 键盘驱动（pynput / humandriver）
│   ├── window/              # 窗口管理驱动（pywin32）
│   └── system/              # 系统信息驱动（psutil）
│       ├── info.py          # 系统信息采集
│       └── process.py       # 进程查询
├── mcp_server/              # MCP 协议层
│   ├── server.py            # FastMCP 服务器创建
│   ├── tool_registry.py     # 工具注册中心
│   ├── prompts.py           # MCP Prompts 定义
│   └── resources.py         # MCP Resources 定义
├── logs/                    # 日志目录
│   ├── computer_mcp.log     # 全量日志
│   ├── crash.log            # 崩溃日志（ERROR 及以上）
│   └── audit.log            # 操作审计日志
├── assets/                  # 资源文件
│   └── screenshots/         # 截图存储
└── tests/                   # 单元测试
```

## 开发计划

### v0.1.0 (当前)
- [x] MCP 服务器基础框架
- [x] 屏幕截图（mss）
- [x] 鼠标控制（pynput + human-mouse）
- [x] 键盘控制（pynput + humandriver）
- [x] 窗口管理（pywin32）
- [x] 系统进程查询（psutil）
- [x] 安全模块
- [x] 坐标系统（绝对 + 归一化 + 多显示器）
- [x] AI 操控浮窗

### v0.2.0
- [ ] Agent 预设模板（浏览器自动化、微信操作等）
- [ ] 操作录制与回放
- [ ] 插件系统

## 安全说明

本项目**仅在本地运行**，不会向任何外部服务发送数据。所有操作受安全模块保护：

- 安全模式默认开启
- 危险操作被拦截并记录
- 每次会话有操作次数上限
- 所有操作写入审计日志

**请勿在不受信任的环境中运行本服务。** MCP Server 拥有完整的电脑操作权限，仅应在可信的本地环境中使用。

## License

MIT License
