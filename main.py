"""computer-mcp 入口。

启动 MCP 服务器，支持 stdio 和 sse 两种传输方式。
使用方式:
    python main.py                     # 默认 stdio 模式
    COMPUTER_MCP_TRANSPORT=sse python main.py  # SSE 模式
"""

from __future__ import annotations

import sys


def main() -> None:
    """启动 MCP 服务器。"""
    # Windows DPI 感知 — 确保坐标系统一致
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-Monitor DPI Aware
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    # 初始化日志（import 时自动触发）
    import config.logging  # noqa: F401

    from loguru import logger
    from config.settings import settings
    from mcp_server.server import create_mcp_server

    logger.info("=" * 60)
    logger.info(f"[启动] computer-mcp v0.1.0")
    logger.info(f"[启动] 传输方式: {settings.transport}")
    logger.info(f"[启动] 鼠标驱动: {settings.mouse_driver}")
    logger.info(f"[启动] 键盘驱动: {settings.keyboard_driver}")
    logger.info(f"[启动] 安全模式: {settings.safe_mode}")
    logger.info(f"[启动] AI 助手: {settings.ai_assistant_name}")
    logger.info("=" * 60)

    # 初始化 AI 操控浮窗
    try:
        from core.overlay import init_overlay
        init_overlay(settings.ai_assistant_name)
        logger.info("[启动] AI 操控浮窗已初始化")
    except Exception as e:
        logger.warning(f"[启动] 浮窗初始化失败（不影响功能）: {e}")

    # 创建 MCP 服务器
    mcp = create_mcp_server()

    # 根据配置选择传输方式
    try:
        if settings.transport == "sse":
            mcp.run(transport="sse")
        else:
            mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("[退出] 用户中断 (Ctrl+C)")
    except Exception as e:
        logger.critical(f"[致命错误] 服务器异常退出: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
