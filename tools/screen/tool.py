"""屏幕工具注册。

将屏幕服务的所有方法注册为 MCP 工具。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

if TYPE_CHECKING:
    from services.screen_service import ScreenService


def register_screen_tools(mcp: FastMCP, screen_service: ScreenService) -> None:
    """注册所有屏幕相关的 MCP 工具。

    Args:
        mcp: FastMCP 实例
        screen_service: 屏幕服务实例
    """

    @mcp.tool()
    async def get_screen_info() -> str:
        """获取所有显示器信息。

        返回所有显示器的分辨率、位置、DPI 缩放等信息。
        """
        return await screen_service.get_screen_info()

    @mcp.tool()
    async def take_screenshot(
        monitor_index: int = 0,
        max_width: int | None = None,
    ) -> str:
        """截取屏幕截图。

        返回截图文件路径、宽高、格式。截图保存在 assets/screenshots/ 目录下。

        Args:
            monitor_index: 显示器索引，0 表示全部（虚拟屏幕）
            max_width: 最大宽度，超出时等比缩放（推荐 1920）
        """
        return await screen_service.take_screenshot(monitor_index, max_width)

    @mcp.tool()
    async def take_region_screenshot(
        x: int,
        y: int,
        width: int,
        height: int,
        max_width: int | None = None,
    ) -> str:
        """截取指定区域的屏幕截图。

        Args:
            x: 区域左上角 X 坐标
            y: 区域左上角 Y 坐标
            width: 区域宽度
            height: 区域高度
            max_width: 最大宽度
        """
        return await screen_service.take_region_screenshot(x, y, width, height, max_width)

    @mcp.tool()
    async def get_mouse_position() -> str:
        """获取当前鼠标位置。

        返回鼠标的绝对像素坐标。
        """
        return await screen_service.get_mouse_position()

    @mcp.tool()
    async def observe() -> str:
        """观察当前电脑状态。

        一次性获取：屏幕信息、鼠标位置、活动窗口、屏幕截图。
        截图保存到文件，返回文件路径。

        推荐工作流：
        1. 调用 observe 获取完整状态（含截图文件路径）
        2. 查看截图文件了解屏幕画面
        3. 根据画面决定下一步操作
        """
        return await screen_service.observe()
