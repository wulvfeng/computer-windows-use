"""schemas 包 — 所有数据模型集中导出。"""

from schemas.keyboard import (
    HotkeyParams,
    KeyDownParams,
    KeyUpParams,
    PressKeyParams,
    TypeTextParams,
)
from schemas.mouse import (
    ClickParams,
    DoubleClickParams,
    DragParams,
    MoveMouseParams,
    RightClickParams,
    ScrollParams,
)
from schemas.screen import (
    AllScreenInfo,
    MousePosition,
    Point,
    Region,
    ScreenInfo,
    ScreenshotResult,
)
from schemas.system import PingResult, SystemInfo
from schemas.window import (
    FocusWindowParams,
    WindowInfo,
    WindowListResult,
    WindowRect,
)

__all__ = [
    # screen
    "Point",
    "ScreenInfo",
    "AllScreenInfo",
    "ScreenshotResult",
    "Region",
    "MousePosition",
    # mouse
    "MoveMouseParams",
    "ClickParams",
    "DoubleClickParams",
    "RightClickParams",
    "DragParams",
    "ScrollParams",
    # keyboard
    "TypeTextParams",
    "PressKeyParams",
    "KeyDownParams",
    "KeyUpParams",
    "HotkeyParams",
    # window
    "WindowInfo",
    "WindowRect",
    "FocusWindowParams",
    "WindowListResult",
    # system
    "SystemInfo",
    "PingResult",
]
