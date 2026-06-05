"""键盘操作的数据模型。

定义文本输入、按键、组合键等操作的参数模型。"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TypeTextParams(BaseModel):
    """文本输入参数。"""

    text: str = Field(description="要输入的文本内容")
    interval: Optional[float] = Field(default=None, description="逐字符输入间隔（秒），None 使用默认值")


class PressKeyParams(BaseModel):
    """单次按键参数。"""

    key: str = Field(description="按键名称，如 enter / tab / f5")


class KeyDownParams(BaseModel):
    """按下按键（不释放）参数。"""

    key: str = Field(description="按键名称")


class KeyUpParams(BaseModel):
    """释放按键参数。"""

    key: str = Field(description="按键名称")


class HotkeyParams(BaseModel):
    """组合键参数。"""

    keys: list[str] = Field(description="按键名称列表，如 ['ctrl', 'c']")
    description: Optional[str] = Field(default=None, description="组合键用途描述（仅用于日志）")
