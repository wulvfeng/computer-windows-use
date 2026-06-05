"""分层异常体系。

所有自定义异常均继承自 ComputerMCPError，按模块拆分为子类，
便于调用方按层级捕获。"""

from __future__ import annotations


# ── 基类 ──────────────────────────────────────────────
class ComputerMCPError(Exception):
    """computer-mcp 顶层异常基类。"""

    def __init__(self, message: str = "", detail: str = "") -> None:
        self.detail = detail
        super().__init__(message)


# ── 驱动层异常 ────────────────────────────────────────
class DriverError(ComputerMCPError):
    """底层驱动调用失败（pynput / mss / pywin32 等）。"""


# ── 鼠标异常 ──────────────────────────────────────────
class MouseError(ComputerMCPError):
    """鼠标操作异常基类。"""


class CoordinateOutOfBoundsError(MouseError):
    """坐标超出屏幕边界。"""


class EmergencyStopError(MouseError):
    """鼠标紧急停止触发。"""


# ── 键盘异常 ──────────────────────────────────────────
class KeyboardError(ComputerMCPError):
    """键盘操作异常基类。"""


class DangerousHotkeyError(KeyboardError):
    """危险快捷键被安全模块拦截。"""


class InvalidKeyError(KeyboardError):
    """无效的按键名称。"""


# ── 屏幕异常 ──────────────────────────────────────────
class ScreenError(ComputerMCPError):
    """屏幕操作异常基类。"""


class ScreenshotError(ScreenError):
    """截图失败。"""


class MonitorNotFoundError(ScreenError):
    """未找到指定显示器。"""


# ── 窗口异常 ──────────────────────────────────────────
class WindowError(ComputerMCPError):
    """窗口操作异常基类。"""


class WindowNotFoundError(WindowError):
    """未找到目标窗口。"""


# ── 系统异常 ──────────────────────────────────────────
class SystemError(ComputerMCPError):
    """系统操作异常基类。"""


# ── 安全异常 ──────────────────────────────────────────
class SecurityError(ComputerMCPError):
    """安全模块拦截异常基类。"""


class ActionLimitExceededError(SecurityError):
    """单次会话操作次数超限。"""

    def __init__(self, limit: int, current: int) -> None:
        self.limit = limit
        self.current = current
        super().__init__(
            f"操作次数超限：当前 {current}，上限 {limit}",
            detail="action_limit_exceeded",
        )
