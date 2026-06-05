"""显示器信息驱动。

使用 mss 获取多显示器信息，支持 DPI 缩放检测。
封装 pywin32 调用获取 DPI 缩放比例。"""

from __future__ import annotations

import ctypes
import ctypes.wintypes
from typing import TYPE_CHECKING

import mss
import mss.tools

if TYPE_CHECKING:
    pass


def get_all_monitors() -> list[dict[str, int | str | float | bool]]:
    """获取所有显示器信息。

    返回:
        显示器信息列表，每个元素包含 index, left, top, width, height, name 等字段。
    """
    with mss.mss() as sct:
        monitors = []
        for idx, mon in enumerate(sct.monitors):
            # mss monitors[0] 是虚拟屏幕（所有显示器合并），从 [1] 开始才是单个显示器
            if idx == 0:
                continue
            monitors.append({
                "index": idx - 1,
                "left": mon["left"],
                "top": mon["top"],
                "width": mon["width"],
                "height": mon["height"],
                "name": mon.get("name", f"Monitor {idx - 1}"),
            })
    return monitors


def get_primary_monitor() -> dict[str, int | str | float | bool]:
    """获取主显示器信息。

    返回:
        主显示器信息字典。
    """
    with mss.mss() as sct:
        mon = sct.monitors[0]  # 虚拟屏幕（包含所有显示器）
        primary = sct.monitors[1] if len(sct.monitors) > 1 else mon
    return {
        "index": 0,
        "left": primary["left"],
        "top": primary["top"],
        "width": primary["width"],
        "height": primary["height"],
        "name": primary.get("name", "Primary"),
    }


def get_virtual_screen() -> dict[str, int]:
    """获取虚拟屏幕（所有显示器合并区域）信息。

    返回:
        虚拟屏幕的 left, top, width, height。
    """
    with mss.mss() as sct:
        mon = sct.monitors[0]
    return {
        "left": mon["left"],
        "top": mon["top"],
        "width": mon["width"],
        "height": mon["height"],
    }


def get_dpi_scale() -> float:
    """获取当前 DPI 缩放比例。

    使用 Win32 API 获取系统 DPI 缩放因子。
    Windows 10 1803+ 支持 Per-Monitor DPI Aware V2。

    Returns:
        DPI 缩放比例，如 1.0（100%）、1.25（125%）、1.5（150%）。
    """
    try:
        # 获取 DPI_AWARENESS_CONTEXT
        user32 = ctypes.windll.user32  # type: ignore[attr-defined]
        # 尝试获取 DPI（96 DPI = 100%）
        # SHGetWorkArea 不受 DPI 影响，使用 GetDpiForSystem
        gdi32 = ctypes.windll.gdi32  # type: ignore[attr-defined]
        dpi = gdi32.GetDeviceCaps(user32.GetDC(0), 88)  # LOGPIXELSX = 88
        user32.ReleaseDC(0, user32.GetDC(0))
        if dpi > 0:
            return round(dpi / 96.0, 2)
    except Exception:
        pass
    return 1.0


def is_point_in_monitor(
    x: int, y: int, monitor: dict[str, int | str | float | bool]
) -> bool:
    """判断坐标是否在指定显示器范围内。

    Args:
        x: X 坐标
        y: Y 坐标
        monitor: 显示器信息字典

    Returns:
        是否在范围内。
    """
    left = int(monitor["left"])
    top = int(monitor["top"])
    width = int(monitor["width"])
    height = int(monitor["height"])
    return left <= x < left + width and top <= y < top + height
