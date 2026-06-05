"""工具注册中心。

负责将所有 Service 层的能力注册为 MCP 工具。
遵循单一职责原则：只负责编排注册，不含业务逻辑。"""

from __future__ import annotations

from loguru import logger
from mcp.server.fastmcp import FastMCP

from core.security import SecurityGuard
from services.screen_service import ScreenService
from services.mouse_service import MouseService
from services.keyboard_service import KeyboardService
from services.window_service import WindowService
from services.system_service import SystemService
from tools.screen.tool import register_screen_tools
from tools.mouse.tool import register_mouse_tools
from tools.keyboard.tool import register_keyboard_tools
from tools.window.tool import register_window_tools
from tools.system.tool import register_system_tools


def register_all_tools(mcp: FastMCP, security: SecurityGuard) -> None:
    """注册所有 MCP 工具。

    按模块创建 Service 实例并委托给对应的 tool 注册函数。

    Args:
        mcp: FastMCP 实例
        security: 安全守卫实例
    """
    logger.info("[ToolRegistry] 开始注册所有工具...")

    # 创建 Service 实例
    screen_service = ScreenService(security)
    mouse_service = MouseService(security)
    keyboard_service = KeyboardService(security)
    window_service = WindowService(security)
    system_service = SystemService(security)

    # 按模块注册工具
    _register = [
        ("screen", register_screen_tools, screen_service),
        ("mouse", register_mouse_tools, mouse_service),
        ("keyboard", register_keyboard_tools, keyboard_service),
        ("window", register_window_tools, window_service),
        ("system", register_system_tools, system_service),
    ]

    for name, func, service in _register:
        try:
            func(mcp, service)
            logger.info(f"[ToolRegistry] {name} 工具注册完成")
        except Exception as e:
            logger.error(f"[ToolRegistry] {name} 工具注册失败: {e}")
            raise

    logger.info("[ToolRegistry] 所有工具注册完成")
