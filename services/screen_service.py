"""屏幕服务。

提供屏幕信息查询、截图、鼠标位置获取、观察等业务逻辑。
协调 driver 层和安全模块。"""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

from loguru import logger

from core.exceptions import ComputerMCPError
from core.result import ToolResult
from schemas.screen import AllScreenInfo, MousePosition, Point, ScreenInfo
from tools.screen import monitor as monitor_driver
from tools.screen.screenshot import (
    save_screenshot,
    take_region_screenshot,
    take_screenshot,
)

if TYPE_CHECKING:
    from core.security import SecurityGuard


class ScreenService:
    """屏幕服务 — 提供屏幕观测和截图能力。"""

    def __init__(self, security: SecurityGuard) -> None:
        self._security = security

    async def get_screen_info(self) -> str:
        """获取所有显示器信息。"""
        with ToolResult.timed() as timer:
            try:
                self._security.check_emergency_stop()

                raw_monitors = monitor_driver.get_all_monitors()
                primary = monitor_driver.get_primary_monitor()
                virtual = monitor_driver.get_virtual_screen()
                dpi_scale = monitor_driver.get_dpi_scale()

                screens = []
                for m in raw_monitors:
                    screens.append(ScreenInfo(
                        index=int(m["index"]),
                        name=str(m["name"]),
                        width=int(m["width"]),
                        height=int(m["height"]),
                        x=int(m["left"]),
                        y=int(m["top"]),
                        dpi_scale=dpi_scale,
                        is_primary=(int(m["index"]) == 0),
                    ))

                primary_info = ScreenInfo(
                    index=0,
                    name=str(primary["name"]),
                    width=int(primary["width"]),
                    height=int(primary["height"]),
                    x=int(primary["left"]),
                    y=int(primary["top"]),
                    dpi_scale=dpi_scale,
                    is_primary=True,
                )

                all_info = AllScreenInfo(
                    screens=screens,
                    primary=primary_info,
                    total_width=int(virtual["width"]),
                    total_height=int(virtual["height"]),
                )

                result = ToolResult.ok(
                    data=all_info.model_dump(),
                    elapsed_ms=0,
                )
                return result.to_mcp_response()

            except ComputerMCPError as e:
                return ToolResult.from_exception(e).to_mcp_response()

    async def take_screenshot(
        self,
        monitor_index: int = 0,
        max_width: int | None = None,
    ) -> str:
        """截取屏幕截图，保存到文件并返回路径。"""
        with ToolResult.timed() as timer:
            try:
                self._security.check_emergency_stop()

                fmt = "png"
                quality = 85

                img_bytes, width, height, fmt = await asyncio.to_thread(
                    take_screenshot,
                    monitor_index,
                    max_width,
                    fmt,
                    quality,
                )

                # 保存到文件，返回路径
                from tools.screen.screenshot import save_screenshot
                file_path = await asyncio.to_thread(
                    save_screenshot, img_bytes, fmt, "screenshot"
                )

                self._security.record_action("screenshot", f"monitor={monitor_index} path={file_path}")

                result_data = {
                    "width": width,
                    "height": height,
                    "format": fmt,
                    "file_path": file_path,
                    "monitor_index": monitor_index,
                }

                result = ToolResult.ok(data=result_data)
                return result.to_mcp_response()

            except ComputerMCPError as e:
                return ToolResult.from_exception(e).to_mcp_response()

    async def take_region_screenshot(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        max_width: int | None = None,
    ) -> str:
        """截取指定区域的屏幕截图，保存到文件并返回路径。"""
        with ToolResult.timed() as timer:
            try:
                self._security.check_emergency_stop()

                img_bytes, w, h, fmt = await asyncio.to_thread(
                    take_region_screenshot,
                    x, y, width, height,
                    max_width,
                    "png",
                    85,
                )

                # 保存到文件，返回路径
                from tools.screen.screenshot import save_screenshot
                file_path = await asyncio.to_thread(
                    save_screenshot, img_bytes, fmt, "region"
                )

                self._security.record_action(
                    "region_screenshot",
                    f"region=({x},{y},{width},{height}) path={file_path}",
                )

                result_data = {
                    "width": w,
                    "height": h,
                    "format": fmt,
                    "file_path": file_path,
                }

                result = ToolResult.ok(data=result_data)
                return result.to_mcp_response()

            except ComputerMCPError as e:
                return ToolResult.from_exception(e).to_mcp_response()

    async def get_mouse_position(self) -> str:
        """获取当前鼠标位置。"""
        try:
            self._security.check_emergency_stop()

            # 通过 mouse driver 获取位置（延迟导入避免循环）
            from config.settings import settings
            if settings.mouse_driver == "human_mouse":
                from tools.mouse.human_mouse_driver import HumanMouseDriver
                driver = HumanMouseDriver()
            else:
                from tools.mouse.pynput_driver import PynputMouseDriver
                driver = PynputMouseDriver()

            x, y = driver.get_position()
            pos = MousePosition(x=x, y=y)

            result = ToolResult.ok(data=pos.model_dump())
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def observe(self) -> str:
        """观察当前电脑状态 — 屏幕信息 + 鼠标位置 + 活动窗口（轻量，不含截图）。"""
        try:
            self._security.check_emergency_stop()

            # 并行获取各项信息
            screen_info_str = await self.get_screen_info()
            mouse_pos_str = await self.get_mouse_position()

            # 获取活动窗口
            from tools.window.manager import get_active_window
            active_win = get_active_window()

            # 解析各项数据
            screen_data = json.loads(screen_info_str)
            mouse_data = json.loads(mouse_pos_str)

            observe_result = {
                "screen_info": screen_data.get("data", {}),
                "mouse_position": mouse_data.get("data", {}),
                "active_window": active_win or {},
                "hint": "需要查看屏幕画面请调用 take_screenshot",
            }

            result = ToolResult.ok(data=observe_result)
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()
