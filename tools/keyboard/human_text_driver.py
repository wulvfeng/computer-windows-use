"""humandriver 键盘驱动。

使用 humandriver 库实现更拟人化的键盘输入。
如果 humandriver 不可用，则回退到 pynput。"""

from __future__ import annotations

import random
import time

from loguru import logger

from tools.keyboard.driver import KeyboardDriver

try:
    from humandriver import HumanDriver  # type: ignore[import-untyped]
    HAS_HUMAN_DRIVER = True
except ImportError:
    HAS_HUMAN_DRIVER = False
    logger.warning("humandriver 未安装，将回退到 pynput 键盘驱动")


class HumanTextKeyboardDriver(KeyboardDriver):
    """基于 humandriver 的键盘驱动（如不可用则回退 pynput）。"""

    def __init__(self) -> None:
        super().__init__()
        self._use_human = HAS_HUMAN_DRIVER
        if self._use_human:
            self._driver = HumanDriver()
        else:
            from tools.keyboard.pynput_driver import PynputKeyboardDriver
            self._fallback = PynputKeyboardDriver()

    def type_text(self, text: str, interval: float | None = None) -> None:
        """输入文本。"""
        if self._use_human:
            self._driver.type_text(text, interval=interval)
        else:
            self._fallback.type_text(text, interval)

    def press_key(self, key: str) -> None:
        """按下并释放一个键。"""
        if self._use_human:
            self._driver.press_key(key)
        else:
            self._fallback.press_key(key)

    def key_down(self, key: str) -> None:
        """按下按键（不释放）。"""
        if self._use_human:
            self._driver.key_down(key)
        else:
            self._fallback.key_down(key)

    def key_up(self, key: str) -> None:
        """释放按键。"""
        if self._use_human:
            self._driver.key_up(key)
        else:
            self._fallback.key_up(key)

    def hotkey(self, keys: list[str]) -> None:
        """按下组合键。"""
        if self._use_human:
            self._driver.hotkey(keys)
        else:
            self._fallback.hotkey(keys)
