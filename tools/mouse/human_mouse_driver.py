"""human-mouse 鼠标驱动。

使用 human-mouse 库实现更拟人化的鼠标移动轨迹。
如果 human-mouse 不可用，则回退到 pynput。"""

from __future__ import annotations

import random
import time
from typing import Optional

from loguru import logger

from tools.mouse.driver import MouseDriver

try:
    from human_mouse import HumanMouse  # type: ignore[import-untyped]
    HAS_HUMAN_MOUSE = True
except ImportError:
    HAS_HUMAN_MOUSE = False
    logger.warning("human-mouse 未安装，将回退到 pynput 驱动")


class HumanMouseDriver(MouseDriver):
    """基于 human-mouse 的鼠标驱动（如不可用则回退 pynput）。"""

    def __init__(self) -> None:
        super().__init__()
        self._use_human = HAS_HUMAN_MOUSE
        if self._use_human:
            self._human = HumanMouse()
        else:
            from pynput.mouse import Button, Controller
            self._mouse = Controller()
            self._Button = Button

    def _get_button(self, name: str):  # type: ignore[no-untyped-def]
        """将字符串按钮名转为按钮对象。"""
        if self._use_human:
            return name.lower()
        mapping = {
            "left": self._Button.left,
            "right": self._Button.right,
            "middle": self._Button.middle,
        }
        return mapping.get(name.lower(), self._Button.left)

    def move_to(self, x: int, y: int, duration: Optional[float] = None) -> None:
        """移动鼠标到指定位置。"""
        if self._use_human:
            dur = duration if duration is not None else random.uniform(
                self._settings.mouse_move_duration_min,
                self._settings.mouse_move_duration_max,
            )
            self._human.move_to(x, y, duration=dur)
        else:
            current_x, current_y = self._mouse.position
            dur = duration or 0.5
            steps = max(1, int(dur / 0.01))
            dx = (x - current_x) / steps
            dy = (y - current_y) / steps
            for i in range(steps):
                nx = int(current_x + dx * (i + 1))
                ny = int(current_y + dy * (i + 1))
                self._mouse.position = (nx, ny)
                time.sleep(dur / steps)
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
        if self._use_human:
            for _ in range(clicks):
                self._human.click(button=self._get_button(button))
        else:
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
        if self._use_human:
            self._human.press(button=btn)
            self.move_to(end_x, end_y, duration)
            self._human.release(button=btn)
        else:
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
        if self._use_human:
            self._human.scroll(clicks)
        else:
            self._mouse.scroll(clicks)

    def get_position(self) -> tuple[int, int]:
        """获取当前鼠标位置。"""
        if self._use_human:
            pos = self._human.get_position()
            return (int(pos[0]), int(pos[1]))
        x, y = self._mouse.position
        return (int(x), int(y))
