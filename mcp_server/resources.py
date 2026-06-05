"""MCP Resources 定义。

为 MCP 客户端提供只读资源，如配置信息、帮助文档等。"""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from config.settings import settings
from config.constants import APP_NAME, APP_VERSION, SPECIAL_KEYS


def register_all_resources(mcp: FastMCP) -> None:
    """注册所有 MCP 资源。

    Args:
        mcp: FastMCP 实例
    """

    @mcp.resource("computer-mcp://config")
    def get_config() -> str:
        """服务配置信息（脱敏）。"""
        config = {
            "server_name": settings.server_name,
            "transport": settings.transport,
            "mouse_driver": settings.mouse_driver,
            "keyboard_driver": settings.keyboard_driver,
            "safe_mode": settings.safe_mode,
            "max_actions_per_session": settings.max_actions_per_session,
            "version": APP_VERSION,
        }
        return json.dumps(config, ensure_ascii=False, indent=2)

    @mcp.resource("computer-mcp://keys")
    def get_supported_keys() -> str:
        """支持的按键名称列表。"""
        keys = sorted(SPECIAL_KEYS)
        return json.dumps({
            "special_keys": keys,
            "usage": "组合键请使用列表格式，如 ['ctrl', 'c']",
            "examples": {
                "复制": ["ctrl", "c"],
                "粘贴": ["ctrl", "v"],
                "全选": ["ctrl", "a"],
                "保存": ["ctrl", "s"],
                "撤销": ["ctrl", "z"],
                "切换窗口": ["alt", "tab"],
                "关闭窗口": ["alt", "f4"],
            },
        }, ensure_ascii=False, indent=2)
