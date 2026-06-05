"""窗口管理的数据模型。

定义窗口信息、窗口操作参数等 Pydantic 模型。"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class WindowRect(BaseModel):
    """窗口位置和大小。"""

    left: int = Field(description="窗口左边 X 坐标")
    top: int = Field(description="窗口顶部 Y 坐标")
    right: int = Field(description="窗口右边 X 坐标")
    bottom: int = Field(description="窗口底部 Y 坐标")
    width: int = Field(description="窗口宽度")
    height: int = Field(description="窗口高度")


class WindowInfo(BaseModel):
    """窗口信息。"""

    handle: int = Field(description="窗口句柄（HWND）")
    title: str = Field(description="窗口标题")
    class_name: str = Field(default="", description="窗口类名")
    process_name: str = Field(default="", description="所属进程名称")
    process_id: int = Field(default=0, description="所属进程 PID")
    rect: Optional[WindowRect] = Field(default=None, description="窗口位置和大小")
    is_visible: bool = Field(default=True, description="是否可见")
    is_active: bool = Field(default=False, description="是否为当前活动窗口")


class FocusWindowParams(BaseModel):
    """聚焦窗口参数。"""

    title: Optional[str] = Field(default=None, description="按窗口标题模糊匹配")
    handle: Optional[int] = Field(default=None, description="按窗口句柄精确匹配")
    raise_window: bool = Field(default=True, description="是否提升窗口层级")


class WindowListResult(BaseModel):
    """窗口列表结果。"""

    windows: list[WindowInfo] = Field(description="窗口列表")
    count: int = Field(description="窗口总数")
