"""鼠标服务。

提供鼠标移动、点击、拖拽、滚动等业务逻辑。
协调 driver 层、安全模块和坐标转换。"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional

from loguru import logger

from config.settings import settings
from core.exceptions import ComputerMCPError
from core.result import ToolResult
from tools.screen import monitor as monitor_driver
from tools.mouse.driver import MouseDriver

if TYPE_CHECKING:
    from core.security import SecurityGuard


class MouseService:
    """鼠标服务 — 提供鼠标操作能力。"""

    def __init__(self, security: SecurityGuard) -> None:
        self._security = security
        self._driver: MouseDriver | None = None

    def _get_driver(self) -> MouseDriver:
        """延迟初始化鼠标驱动。"""
        if self._driver is None:
            if settings.mouse_driver == "human_mouse":
                from tools.mouse.human_mouse_driver import HumanMouseDriver
                self._driver = HumanMouseDriver()
            else:
                from tools.mouse.pynput_driver import PynputMouseDriver
                self._driver = PynputMouseDriver()
            logger.info(f"鼠标驱动已初始化: {self._driver.name}")
        return self._driver

    def _resolve_position(
        self,
        x: float | None,
        y: float | None,
        normalized: bool,
    ) -> tuple[int, int]:
        """将坐标转为绝对像素坐标。

        如果 x, y 为 None，返回当前鼠标位置。
        归一化坐标 (0~1) 基于主显示器分辨率转换。
        """
        if x is None or y is None:
            return self._get_driver().get_position()

        if normalized:
            # 归一化坐标基于主显示器
            primary = monitor_driver.get_primary_monitor()
            abs_x = int(x * primary["width"])
            abs_y = int(y * primary["height"])
        else:
            abs_x = int(x)
            abs_y = int(y)

        # 安全校验
        virtual = monitor_driver.get_virtual_screen()
        self._security.check_coordinate_bounds(
            abs_x, abs_y, virtual["width"], virtual["height"]
        )

        return abs_x, abs_y

    async def move_mouse(
        self,
        x: float,
        y: float,
        normalized: bool = False,
        duration: float | None = None,
    ) -> str:
        """移动鼠标到指定位置。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            abs_x, abs_y = self._resolve_position(x, y, normalized)
            driver = self._get_driver()

            await asyncio.to_thread(driver.move_to, abs_x, abs_y, duration)
            self._security.record_action("move_mouse", f"to=({abs_x},{abs_y})")

            result = ToolResult.ok(data={"x": abs_x, "y": abs_y})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def click(
        self,
        x: float | None = None,
        y: float | None = None,
        normalized: bool = False,
        button: str = "left",
        clicks: int = 1,
    ) -> str:
        """在指定位置点击鼠标。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            abs_x, abs_y = self._resolve_position(x, y, normalized)
            driver = self._get_driver()

            await asyncio.to_thread(driver.click, abs_x, abs_y, button, clicks)
            self._security.record_action(
                "click",
                f"pos=({abs_x},{abs_y}) button={button} clicks={clicks}",
            )

            result = ToolResult.ok(data={"x": abs_x, "y": abs_y, "button": button})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def double_click(
        self,
        x: float | None = None,
        y: float | None = None,
        normalized: bool = False,
        button: str = "left",
    ) -> str:
        """在指定位置双击鼠标。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            abs_x, abs_y = self._resolve_position(x, y, normalized)
            driver = self._get_driver()

            await asyncio.to_thread(driver.double_click, abs_x, abs_y, button)
            self._security.record_action(
                "double_click",
                f"pos=({abs_x},{abs_y}) button={button}",
            )

            result = ToolResult.ok(data={"x": abs_x, "y": abs_y, "button": button})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def right_click(
        self,
        x: float | None = None,
        y: float | None = None,
        normalized: bool = False,
    ) -> str:
        """在指定位置右键点击。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            abs_x, abs_y = self._resolve_position(x, y, normalized)
            driver = self._get_driver()

            await asyncio.to_thread(driver.right_click, abs_x, abs_y)
            self._security.record_action("right_click", f"pos=({abs_x},{abs_y})")

            result = ToolResult.ok(data={"x": abs_x, "y": abs_y})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def drag(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        normalized: bool = False,
        duration: float | None = None,
        button: str = "left",
    ) -> str:
        """从起始位置拖拽到结束位置。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            s_x, s_y = self._resolve_position(start_x, start_y, normalized)
            e_x, e_y = self._resolve_position(end_x, end_y, normalized)
            driver = self._get_driver()

            await asyncio.to_thread(
                driver.drag, s_x, s_y, e_x, e_y, duration, button
            )
            self._security.record_action(
                "drag",
                f"from=({s_x},{s_y}) to=({e_x},{e_y})",
            )

            result = ToolResult.ok(data={
                "start": {"x": s_x, "y": s_y},
                "end": {"x": e_x, "y": e_y},
                "button": button,
            })
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def scroll(
        self,
        clicks: int,
        x: float | None = None,
        y: float | None = None,
        normalized: bool = False,
    ) -> str:
        """滚动鼠标滚轮。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            if x is not None and y is not None:
                abs_x, abs_y = self._resolve_position(x, y, normalized)
            else:
                abs_x, abs_y = None, None

            driver = self._get_driver()
            await asyncio.to_thread(driver.scroll, clicks, abs_x, abs_y)
            self._security.record_action(
                "scroll",
                f"clicks={clicks} pos=({abs_x},{abs_y})",
            )

            result = ToolResult.ok(data={"clicks": clicks})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()
