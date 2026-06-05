"""鼠标工具注册。

将鼠标服务的所有方法注册为 MCP 工具。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

if TYPE_CHECKING:
    from services.mouse_service import MouseService


def register_mouse_tools(mcp: FastMCP, mouse_service: MouseService) -> None:
    """注册所有鼠标相关的 MCP 工具。

    Args:
        mcp: FastMCP 实例
        mouse_service: 鼠标服务实例
    """

    @mcp.tool()
    async def move_mouse(
        x: float,
        y: float,
        normalized: bool = False,
        duration: float | None = None,
    ) -> str:
        """移动鼠标到指定位置。

        支持绝对坐标和归一化坐标。
        绝对坐标：x=1000, y=500 表示屏幕像素位置。
        归一化坐标：x=0.5, y=0.4, normalized=true 表示屏幕中心偏左上。

        Args:
            x: X 坐标
            y: Y 坐标
            normalized: 是否为归一化坐标（0.0~1.0）
            duration: 移动耗时（秒），None 使用默认值
        """
        return await mouse_service.move_mouse(x, y, normalized, duration)

    @mcp.tool()
    async def click(
        x: float | None = None,
        y: float | None = None,
        normalized: bool = False,
        button: str = "left",
        clicks: int = 1,
    ) -> str:
        """在指定位置点击鼠标。

        如果不传 x, y，则在当前鼠标位置点击。

        Args:
            x: X 坐标（None 表示当前位置）
            y: Y 坐标（None 表示当前位置）
            normalized: 是否为归一化坐标
            button: 鼠标按钮 left / right / middle
            clicks: 点击次数
        """
        return await mouse_service.click(x, y, normalized, button, clicks)

    @mcp.tool()
    async def double_click(
        x: float | None = None,
        y: float | None = None,
        normalized: bool = False,
        button: str = "left",
    ) -> str:
        """在指定位置双击鼠标。

        Args:
            x: X 坐标（None 表示当前位置）
            y: Y 坐标（None 表示当前位置）
            normalized: 是否为归一化坐标
            button: 鼠标按钮
        """
        return await mouse_service.double_click(x, y, normalized, button)

    @mcp.tool()
    async def right_click(
        x: float | None = None,
        y: float | None = None,
        normalized: bool = False,
    ) -> str:
        """在指定位置右键点击。

        Args:
            x: X 坐标（None 表示当前位置）
            y: Y 坐标（None 表示当前位置）
            normalized: 是否为归一化坐标
        """
        return await mouse_service.right_click(x, y, normalized)

    @mcp.tool()
    async def drag(
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        normalized: bool = False,
        duration: float | None = None,
        button: str = "left",
    ) -> str:
        """从起始位置拖拽到结束位置。

        Args:
            start_x: 起始 X 坐标
            start_y: 起始 Y 坐标
            end_x: 结束 X 坐标
            end_y: 结束 Y 坐标
            normalized: 是否为归一化坐标
            duration: 拖拽耗时（秒）
            button: 拖拽按钮
        """
        return await mouse_service.drag(
            start_x, start_y, end_x, end_y, normalized, duration, button
        )

    @mcp.tool()
    async def scroll(
        clicks: int,
        x: float | None = None,
        y: float | None = None,
        normalized: bool = False,
    ) -> str:
        """滚动鼠标滚轮。

        正数向上滚动，负数向下滚动。

        Args:
            clicks: 滚动量
            x: 滚动位置 X（None 表示当前位置）
            y: 滚动位置 Y（None 表示当前位置）
            normalized: 是否为归一化坐标
        """
        return await mouse_service.scroll(clicks, x, y, normalized)
