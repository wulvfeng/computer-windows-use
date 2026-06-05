"""MCP 服务器核心。

使用 FastMCP 构建 MCP 服务器，初始化所有服务和工具注册。
这是整个项目的 MCP 入口层。"""

from __future__ import annotations

import time

from loguru import logger
from mcp.server.fastmcp import FastMCP

from config.settings import settings
from core.security import SecurityGuard
from mcp_server.tool_registry import register_all_tools
from mcp_server.prompts import register_all_prompts
from mcp_server.resources import register_all_resources


def create_mcp_server() -> FastMCP:
    """创建并配置 MCP 服务器实例。

    Returns:
        已注册所有工具、提示词、资源的 FastMCP 实例。
    """
    logger.info("[MCP] 正在创建 MCP 服务器...")

    # 创建 FastMCP 实例
    mcp = FastMCP(
        name=settings.server_name,
        instructions=_build_instructions(),
    )

    # 初始化安全守卫
    security = SecurityGuard(settings)

    # 注册所有工具
    register_all_tools(mcp, security)

    # 注册提示词
    register_all_prompts(mcp)

    # 注册资源
    register_all_resources(mcp)

    logger.info("[MCP] 服务器创建完成，等待连接...")
    return mcp


def _build_instructions() -> str:
    """构建 MCP 服务器的说明信息。

    当客户端连接时，会收到这段说明，帮助模型理解如何使用工具。
    """
    return f"""# Computer MCP Server v{settings.server_name}

你是一个 Windows 电脑操作助手。你可以通过以下工具操控用户的电脑：

## 屏幕工具
- **get_screen_info**: 获取显示器信息
- **take_screenshot**: 截取全屏
- **take_region_screenshot**: 截取指定区域
- **get_mouse_position**: 获取鼠标位置
- **observe**: 一次性获取完整电脑状态（含截图，推荐首选调用）

## 鼠标工具
- **move_mouse**: 移动鼠标
- **click**: 点击
- **double_click**: 双击
- **right_click**: 右键点击
- **drag**: 拖拽
- **scroll**: 滚轮

## 键盘工具
- **type_text**: 输入文本
- **press_key**: 按键
- **key_down**: 按下不放
- **key_up**: 释放按键
- **hotkey**: 组合键（如 Ctrl+C）

## 窗口工具
- **list_windows**: 列出所有窗口
- **active_window**: 获取活动窗口
- **focus_window**: 聚焦窗口
- **window_rect**: 获取窗口位置

## 系统工具
- **sleep**: 等待
- **ping**: 健康检查
- **list_processes**: 列出运行中的进程
- **find_process**: 查找某个应用是否在运行
- **get_system_stats**: 获取 CPU/内存/磁盘使用率

## 安全限制
- 危险快捷键（如 Alt+F4）会被拦截
- 每次会话有操作次数上限（{settings.max_actions_per_session}）
- 安全模式下所有操作受审计
"""
