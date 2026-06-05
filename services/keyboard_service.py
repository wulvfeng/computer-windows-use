"""键盘服务。

提供文本输入、按键、组合键等业务逻辑。
协调 driver 层和安全模块（危险快捷键拦截）。"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from loguru import logger

from config.settings import settings
from core.exceptions import ComputerMCPError
from core.result import ToolResult
from tools.keyboard.driver import KeyboardDriver

if TYPE_CHECKING:
    from core.security import SecurityGuard


class KeyboardService:
    """键盘服务 — 提供键盘操作能力。"""

    def __init__(self, security: SecurityGuard) -> None:
        self._security = security
        self._driver: KeyboardDriver | None = None

    def _get_driver(self) -> KeyboardDriver:
        """延迟初始化键盘驱动。"""
        if self._driver is None:
            if settings.keyboard_driver == "humandriver":
                from tools.keyboard.human_text_driver import HumanTextKeyboardDriver
                self._driver = HumanTextKeyboardDriver()
            else:
                from tools.keyboard.pynput_driver import PynputKeyboardDriver
                self._driver = PynputKeyboardDriver()
            logger.info(f"键盘驱动已初始化: {self._driver.name}")
        return self._driver

    async def type_text(
        self,
        text: str,
        interval: float | None = None,
    ) -> str:
        """输入文本内容。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            driver = self._get_driver()
            await asyncio.to_thread(driver.type_text, text, interval)
            self._security.record_action("type_text", f"length={len(text)}")

            result = ToolResult.ok(data={"typed_length": len(text)})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def press_key(self, key: str) -> str:
        """按下并释放一个键。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            driver = self._get_driver()
            await asyncio.to_thread(driver.press_key, key)
            self._security.record_action("press_key", f"key={key}")

            result = ToolResult.ok(data={"key": key})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def key_down(self, key: str) -> str:
        """按下按键（不释放）。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            driver = self._get_driver()
            await asyncio.to_thread(driver.key_down, key)
            self._security.record_action("key_down", f"key={key}")

            result = ToolResult.ok(data={"key": key, "state": "down"})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def key_up(self, key: str) -> str:
        """释放按键。"""
        try:
            self._security.check_emergency_stop()

            driver = self._get_driver()
            await asyncio.to_thread(driver.key_up, key)
            self._security.record_action("key_up", f"key={key}")

            result = ToolResult.ok(data={"key": key, "state": "up"})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def hotkey(
        self,
        keys: list[str],
        description: str | None = None,
    ) -> str:
        """按下组合键。"""
        try:
            self._security.check_emergency_stop()
            self._security.check_action_allowed()

            # 安全模块拦截危险快捷键
            self._security.check_hotkey_safe(keys)

            driver = self._get_driver()
            await asyncio.to_thread(driver.hotkey, keys)
            self._security.record_action(
                "hotkey",
                f"keys={'+'.join(keys)} desc={description or ''}",
            )

            result = ToolResult.ok(data={"keys": keys})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()
