"""鼠标驱动抽象基类。

定义鼠标驱动的统一接口，支持 pynput 和 human-mouse 两种实现。
遵循开闭原则，新增驱动只需继承此基类。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from config.settings import settings


class MouseDriver(ABC):
    """鼠标驱动抽象基类。

    所有鼠标驱动实现必须继承此基类并实现所有抽象方法。
    """

    def __init__(self) -> None:
        self._settings = settings

    @abstractmethod
    def move_to(self, x: int, y: int, duration: Optional[float] = None) -> None:
        """移动鼠标到绝对坐标。

        Args:
            x: 目标 X 坐标
            y: 目标 Y 坐标
            duration: 移动耗时（秒），None 使用默认值
        """
        ...

    @abstractmethod
    def click(
        self,
        x: int,
        y: int,
        button: str = "left",
        clicks: int = 1,
    ) -> None:
        """在指定位置点击鼠标。

        Args:
            x: X 坐标
            y: Y 坐标
            button: 按钮 left / right / middle
            clicks: 点击次数
        """
        ...

    @abstractmethod
    def double_click(self, x: int, y: int, button: str = "left") -> None:
        """在指定位置双击鼠标。"""
        ...

    @abstractmethod
    def right_click(self, x: int, y: int) -> None:
        """在指定位置右键点击。"""
        ...

    @abstractmethod
    def drag(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: Optional[float] = None,
        button: str = "left",
    ) -> None:
        """从起始位置拖拽到结束位置。

        Args:
            start_x: 起始 X
            start_y: 起始 Y
            end_x: 结束 X
            end_y: 结束 Y
            duration: 拖拽耗时（秒）
            button: 拖拽按钮
        """
        ...

    @abstractmethod
    def scroll(
        self,
        clicks: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> None:
        """滚动鼠标滚轮。

        Args:
            clicks: 滚动量，正数向上，负数向下
            x: 滚动位置 X，None 表示当前鼠标位置
            y: 滚动位置 Y，None 表示当前鼠标位置
        """
        ...

    @abstractmethod
    def get_position(self) -> tuple[int, int]:
        """获取当前鼠标位置。

        Returns:
            (x, y) 坐标元组
        """
        ...

    @property
    def name(self) -> str:
        """驱动名称。"""
        return self.__class__.__name__
