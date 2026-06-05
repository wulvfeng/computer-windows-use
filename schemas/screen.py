"""屏幕相关的数据模型。

定义坐标点、屏幕信息、截图结果等 Pydantic 模型。
支持绝对坐标和归一化坐标两种模式。"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Point(BaseModel):
    """坐标点，支持绝对坐标和归一化坐标。"""

    x: float = Field(description="X 坐标（绝对像素值或归一化 0~1）")
    y: float = Field(description="Y 坐标（绝对像素值或归一化 0~1）")
    normalized: bool = Field(default=False, description="是否为归一化坐标（0.0~1.0）")


class ScreenInfo(BaseModel):
    """单个显示器信息。"""

    index: int = Field(description="显示器索引")
    name: str = Field(default="", description="显示器名称")
    width: int = Field(description="物理像素宽度")
    height: int = Field(description="物理像素高度")
    x: int = Field(default=0, description="显示器左上角 X 偏移（多显示器时非零）")
    y: int = Field(default=0, description="显示器左上角 Y 偏移（多显示器时非零）")
    dpi_scale: float = Field(default=1.0, description="DPI 缩放比例（1.0 = 100%）")
    is_primary: bool = Field(default=False, description="是否为主显示器")


class AllScreenInfo(BaseModel):
    """所有显示器汇总信息。"""

    screens: list[ScreenInfo] = Field(description="所有显示器列表")
    primary: ScreenInfo = Field(description="主显示器信息")
    total_width: int = Field(description="所有显示器合并后的总宽度")
    total_height: int = Field(description="所有显示器合并后的总高度")


class ScreenshotResult(BaseModel):
    """截图结果。"""

    width: int = Field(description="截图宽度（像素）")
    height: int = Field(description="截图高度（像素）")
    format: str = Field(description="图片格式：png / jpeg")
    file_path: str = Field(description="截图文件保存路径")
    monitor_index: int = Field(default=0, description="截图的显示器索引，0 表示全部")


class Region(BaseModel):
    """屏幕区域矩形。"""

    x: int = Field(description="区域左上角 X 坐标")
    y: int = Field(description="区域左上角 Y 坐标")
    width: int = Field(description="区域宽度")
    height: int = Field(description="区域高度")


class MousePosition(BaseModel):
    """鼠标当前位置。"""

    x: int = Field(description="鼠标 X 坐标（像素）")
    y: int = Field(description="鼠标 Y 坐标（像素）")
