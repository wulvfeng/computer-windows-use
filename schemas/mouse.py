"""鼠标操作的数据模型。

定义鼠标移动、点击、拖拽、滚轮等操作的参数模型。"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from schemas.screen import Point


class MoveMouseParams(BaseModel):
    """鼠标移动参数。"""

    target: Point = Field(description="目标坐标（绝对或归一化）")
    duration: Optional[float] = Field(default=None, description="移动耗时（秒），None 使用默认值")


class ClickParams(BaseModel):
    """鼠标点击参数。"""

    position: Optional[Point] = Field(default=None, description="点击位置，None 表示当前鼠标位置")
    button: str = Field(default="left", description="按钮：left / right / middle")
    clicks: int = Field(default=1, description="点击次数")


class DoubleClickParams(BaseModel):
    """鼠标双击参数。"""

    position: Optional[Point] = Field(default=None, description="点击位置")
    button: str = Field(default="left", description="按钮：left / right / middle")


class RightClickParams(BaseModel):
    """鼠标右键点击参数。"""

    position: Optional[Point] = Field(default=None, description="点击位置")


class DragParams(BaseModel):
    """鼠标拖拽参数。"""

    start: Point = Field(description="起始坐标")
    end: Point = Field(description="结束坐标")
    duration: Optional[float] = Field(default=None, description="拖拽耗时（秒）")
    button: str = Field(default="left", description="拖拽按钮")


class ScrollParams(BaseModel):
    """鼠标滚轮参数。"""

    clicks: int = Field(description="滚动量，正数向上，负数向下")
    position: Optional[Point] = Field(default=None, description="滚动位置，None 表示当前鼠标位置")
