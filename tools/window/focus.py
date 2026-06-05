"""窗口聚焦驱动。

使用 pywin32 实现窗口聚焦、提升层级等操作。
封装 Win32 API 的 SetForegroundWindow、ShowWindow 等调用。"""

from __future__ import annotations

from typing import Optional

import win32con
import win32gui

from core.exceptions import WindowNotFoundError


def focus_window(
    hwnd: Optional[int] = None,
    title: Optional[str] = None,
    raise_window: bool = True,
) -> int:
    """聚焦指定窗口。

    支持按窗口句柄精确匹配或按标题模糊匹配。
    如果窗口已最小化，会先恢复再聚焦。

    Args:
        hwnd: 窗口句柄（精确匹配）
        title: 窗口标题（模糊匹配，不区分大小写）
        raise_window: 是否提升窗口层级

    Returns:
        成功聚焦的窗口句柄

    Raises:
        WindowNotFoundError: 未找到目标窗口或参数无效
    """
    target_hwnd: Optional[int] = None

    if hwnd:
        # 按句柄精确匹配
        if win32gui.IsWindow(hwnd):
            target_hwnd = hwnd
    elif title:
        # 按标题模糊匹配
        title_lower = title.lower()

        def _find_by_title(h: int, _: int) -> bool:
            nonlocal target_hwnd
            if win32gui.IsWindowVisible(h):
                win_title = win32gui.GetWindowText(h).lower()
                if title_lower in win_title:
                    target_hwnd = h
                    return False  # 停止枚举
            return True

        win32gui.EnumWindows(_find_by_title, None)
    else:
        raise WindowNotFoundError("必须提供 hwnd 或 title 参数", detail="no_target")

    if not target_hwnd:
        raise WindowNotFoundError(
            f"未找到匹配的窗口: hwnd={hwnd}, title={title}",
            detail="window_not_found",
        )

    # 执行聚焦
    if raise_window:
        # 如果窗口最小化，先恢复到正常大小
        if win32gui.IsIconic(target_hwnd):
            win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(target_hwnd)
    else:
        win32gui.SetForegroundWindow(target_hwnd)

    return target_hwnd


def activate_window(hwnd: int) -> None:
    """强制激活窗口（不恢复最小化状态）。

    Args:
        hwnd: 窗口句柄

    Raises:
        WindowNotFoundError: 无效的窗口句柄
    """
    if not win32gui.IsWindow(hwnd):
        raise WindowNotFoundError(
            f"无效的窗口句柄: {hwnd}",
            detail="invalid_hwnd",
        )
    win32gui.SetForegroundWindow(hwnd)


def minimize_window(hwnd: int) -> None:
    """最小化指定窗口。

    Args:
        hwnd: 窗口句柄

    Raises:
        WindowNotFoundError: 无效的窗口句柄
    """
    if not win32gui.IsWindow(hwnd):
        raise WindowNotFoundError(
            f"无效的窗口句柄: {hwnd}",
            detail="invalid_hwnd",
        )
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def restore_window(hwnd: int) -> None:
    """恢复（取消最小化）指定窗口。

    Args:
        hwnd: 窗口句柄

    Raises:
        WindowNotFoundError: 无效的窗口句柄
    """
    if not win32gui.IsWindow(hwnd):
        raise WindowNotFoundError(
            f"无效的窗口句柄: {hwnd}",
            detail="invalid_hwnd",
        )
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
