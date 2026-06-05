"""窗口管理服务。

提供窗口枚举、聚焦、查询等业务逻辑。
协调 window manager driver 和安全模块。"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from loguru import logger

from core.exceptions import ComputerMCPError
from core.result import ToolResult
from tools.window import manager as window_manager
from tools.window import focus as window_focus

if TYPE_CHECKING:
    from core.security import SecurityGuard


class WindowService:
    """窗口管理服务 — 提供窗口操作能力。"""

    def __init__(self, security: SecurityGuard) -> None:
        self._security = security

    async def list_windows(self) -> str:
        """列出所有可见窗口。"""
        try:
            self._security.check_emergency_stop()

            windows = await asyncio.to_thread(window_manager.list_windows)

            result = ToolResult.ok(data={
                "windows": windows,
                "count": len(windows),
            })
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def active_window(self) -> str:
        """获取当前活动窗口信息。"""
        try:
            self._security.check_emergency_stop()

            win = await asyncio.to_thread(window_manager.get_active_window)

            if win is None:
                result = ToolResult.ok(data={"message": "无活动窗口"})
            else:
                result = ToolResult.ok(data=win)

            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def focus_window(
        self,
        title: str | None = None,
        handle: int | None = None,
        raise_window: bool = True,
    ) -> str:
        """聚焦指定窗口。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            hwnd = await asyncio.to_thread(
                window_focus.focus_window,
                handle,
                title,
                raise_window,
            )

            self._security.record_action(
                "focus_window",
                f"hwnd={hwnd} title={title}",
            )

            result = ToolResult.ok(data={
                "handle": hwnd,
                "title": title,
                "focused": True,
            })
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def window_rect(self, handle: int) -> str:
        """获取指定窗口的位置和大小。"""
        try:
            self._security.check_emergency_stop()

            rect = await asyncio.to_thread(
                window_manager.get_window_rect, handle
            )

            result = ToolResult.ok(data=rect)
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()
