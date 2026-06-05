"""窗口管理驱动。

使用 pywin32 实现窗口枚举、查询等操作。
封装 Win32 API 调用。"""

from __future__ import annotations

from typing import Optional

import psutil
import win32gui
import win32process

from core.exceptions import WindowNotFoundError


def list_windows() -> list[dict]:
    """枚举所有可见窗口。

    返回:
        窗口信息列表。
    """
    windows: list[dict] = []

    def _enum_callback(hwnd: int, _: int) -> bool:
        if not win32gui.IsWindowVisible(hwnd):
            return True

        title = win32gui.GetWindowText(hwnd)
        if not title:
            return True

        class_name = win32gui.GetClassName(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top

        # 获取进程信息
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process_name = ""
        try:
            proc = psutil.Process(pid)
            process_name = proc.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        windows.append({
            "handle": hwnd,
            "title": title,
            "class_name": class_name,
            "process_name": process_name,
            "process_id": pid,
            "rect": {
                "left": left,
                "top": top,
                "right": right,
                "bottom": bottom,
                "width": width,
                "height": height,
            },
            "is_visible": True,
            "is_active": hwnd == win32gui.GetForegroundWindow(),
        })
        return True

    win32gui.EnumWindows(_enum_callback, None)
    return windows


def get_active_window() -> Optional[dict]:
    """获取当前活动窗口信息。

    Returns:
        活动窗口信息字典，无活动窗口时返回 None。
    """
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None

    title = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect

    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    process_name = ""
    try:
        proc = psutil.Process(pid)
        process_name = proc.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    return {
        "handle": hwnd,
        "title": title,
        "class_name": class_name,
        "process_name": process_name,
        "process_id": pid,
        "rect": {
            "left": left,
            "top": top,
            "right": right,
            "bottom": bottom,
            "width": right - left,
            "height": bottom - top,
        },
        "is_visible": win32gui.IsWindowVisible(hwnd),
        "is_active": True,
    }


def get_window_rect(hwnd: int) -> dict[str, int]:
    """获取窗口的位置和大小。

    Args:
        hwnd: 窗口句柄

    Returns:
        包含 left, top, right, bottom, width, height 的字典

    Raises:
        WindowNotFoundError: 无效的窗口句柄
    """
    if not win32gui.IsWindow(hwnd):
        raise WindowNotFoundError(
            f"无效的窗口句柄: {hwnd}",
            detail="invalid_hwnd",
        )

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return {
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "width": right - left,
        "height": bottom - top,
    }
