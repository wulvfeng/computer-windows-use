"""pynput 鼠标驱动。

使用 pynput 库实现鼠标操作。"""

from __future__ import annotations

import random
import time
from typing import Optional

from pynput.mouse import Button, Controller, Listener

from tools.mouse.driver import MouseDriver


class PynputMouseDriver(MouseDriver):
    """基于 pynput 的鼠标驱动。"""

    def __init__(self) -> None:
        super().__init__()
        self._mouse = Controller()

    def _get_button(self, name: str) -> Button:
        """将字符串按钮名转为 pynput Button。"""
        mapping = {
            "left": Button.left,
            "right": Button.right,
            "middle": Button.middle,
        }
        return mapping.get(name.lower(), Button.left)

    def move_to(self, x: int, y: int, duration: Optional[float] = None) -> None:
        """移动鼠标到绝对坐标。支持线性插值模拟平滑移动。"""
        dur = duration if duration is not None else random.uniform(
            self._settings.mouse_move_duration_min,
            self._settings.mouse_move_duration_max,
        )

        current_x, current_y = self._mouse.position
        steps = max(1, int(dur / 0.01))
        dx = (x - current_x) / steps
        dy = (y - current_y) / steps

        for i in range(steps):
            jitter_x = random.uniform(-self._settings.mouse_jitter, self._settings.mouse_jitter)
            jitter_y = random.uniform(-self._settings.mouse_jitter, self._settings.mouse_jitter)
            nx = int(current_x + dx * (i + 1) + jitter_x)
            ny = int(current_y + dy * (i + 1) + jitter_y)
            self._mouse.position = (nx, ny)
            time.sleep(dur / steps)

        # 最终精确定位
        self._mouse.position = (x, y)

    def click(
        self,
        x: int,
        y: int,
        button: str = "left",
        clicks: int = 1,
    ) -> None:
        """在指定位置点击鼠标。"""
        self.move_to(x, y)
        time.sleep(self._settings.mouse_click_delay)
        btn = self._get_button(button)
        self._mouse.click(btn, clicks)

    def double_click(self, x: int, y: int, button: str = "left") -> None:
        """在指定位置双击鼠标。"""
        self.click(x, y, button, clicks=2)

    def right_click(self, x: int, y: int) -> None:
        """在指定位置右键点击。"""
        self.click(x, y, button="right", clicks=1)

    def drag(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: Optional[float] = None,
        button: str = "left",
    ) -> None:
        """从起始位置拖拽到结束位置。"""
        self.move_to(start_x, start_y)
        time.sleep(self._settings.mouse_click_delay)
        btn = self._get_button(button)
        self._mouse.press(btn)
        self.move_to(end_x, end_y, duration)
        self._mouse.release(btn)

    def scroll(
        self,
        clicks: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> None:
        """滚动鼠标滚轮。"""
        if x is not None and y is not None:
            self.move_to(x, y)
        self._mouse.scroll(clicks)

    def get_position(self) -> tuple[int, int]:
        """获取当前鼠标位置。"""
        x, y = self._mouse.position
        return (int(x), int(y))
