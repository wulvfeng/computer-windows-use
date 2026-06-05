"""窗口工具注册。

将窗口服务的所有方法注册为 MCP 工具。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

if TYPE_CHECKING:
    from services.window_service import WindowService


def register_window_tools(mcp: FastMCP, window_service: WindowService) -> None:
    """注册所有窗口管理相关的 MCP 工具。

    Args:
        mcp: FastMCP 实例
        window_service: 窗口服务实例
    """

    @mcp.tool()
    async def list_windows() -> str:
        """列出所有可见窗口。

        返回所有可见窗口的标题、句柄、进程名、位置等信息。
        """
        return await window_service.list_windows()

    @mcp.tool()
    async def active_window() -> str:
        """获取当前活动窗口信息。

        返回当前前台窗口的详细信息，包括标题、句柄、位置等。
        """
        return await window_service.active_window()

    @mcp.tool()
    async def focus_window(
        title: str | None = None,
        handle: int | None = None,
        raise_window: bool = True,
    ) -> str:
        """聚焦指定窗口。

        按标题模糊匹配或按句柄精确匹配窗口，将其设为前台窗口。

        Args:
            title: 窗口标题（模糊匹配）
            handle: 窗口句柄（精确匹配）
            raise_window: 是否提升窗口层级
        """
        return await window_service.focus_window(title, handle, raise_window)

    @mcp.tool()
    async def window_rect(handle: int) -> str:
        """获取指定窗口的位置和大小。

        Args:
            handle: 窗口句柄
        """
        return await window_service.window_rect(handle)
