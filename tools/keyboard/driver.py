"""键盘驱动抽象基类。

定义键盘驱动的统一接口，支持 pynput 和 humandriver 两种实现。"""

from __future__ import annotations

from abc import ABC, abstractmethod

from config.settings import settings


class KeyboardDriver(ABC):
    """键盘驱动抽象基类。

    所有键盘驱动实现必须继承此基类并实现所有抽象方法。
    """

    def __init__(self) -> None:
        self._settings = settings

    @abstractmethod
    def type_text(self, text: str, interval: float | None = None) -> None:
        """输入文本。

        Args:
            text: 要输入的文本
            interval: 逐字符间隔（秒），None 使用默认值
        """
        ...

    @abstractmethod
    def press_key(self, key: str) -> None:
        """按下并释放一个键。

        Args:
            key: 按键名称
        """
        ...

    @abstractmethod
    def key_down(self, key: str) -> None:
        """按下按键（不释放）。

        Args:
            key: 按键名称
        """
        ...

    @abstractmethod
    def key_up(self, key: str) -> None:
        """释放按键。

        Args:
            key: 按键名称
        """
        ...

    @abstractmethod
    def hotkey(self, keys: list[str]) -> None:
        """按下组合键。

        Args:
            keys: 按键名称列表，如 ["ctrl", "c"]
        """
        ...

    @property
    def name(self) -> str:
        """驱动名称。"""
        return self.__class__.__name__
