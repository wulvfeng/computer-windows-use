"""常量定义。

集中管理不可变常量：键名映射、DPI 缩放表、默认参数值等。
业务代码通过 import 引用，禁止硬编码字符串。"""

from __future__ import annotations

from typing import Final

# ── 项目信息 ──────────────────────────────────────────
APP_NAME: Final[str] = "computer-mcp"
APP_VERSION: Final[str] = "0.1.0"

# ── 键盘键名映射 ─────────────────────────────────────
# pynput 键名 → 用户友好名 的双向映射
KEY_NAME_MAP: Final[dict[str, str]] = {
    "enter": "enter",
    "return": "enter",
    "tab": "tab",
    "space": "space",
    "backspace": "backspace",
    "delete": "delete",
    "escape": "escape",
    "esc": "escape",
    "ctrl": "ctrl",
    "ctrl_l": "ctrl",
    "ctrl_r": "ctrl",
    "alt": "alt",
    "alt_l": "alt",
    "alt_gr": "alt",
    "shift": "shift",
    "shift_l": "shift",
    "shift_r": "shift",
    "cmd": "cmd",
    "cmd_l": "cmd",
    "cmd_r": "cmd",
    "win": "cmd",
    "win_l": "cmd",
    "win_r": "cmd",
    "caps_lock": "caps_lock",
    "num_lock": "num_lock",
    "scroll_lock": "scroll_lock",
    "print_screen": "print_screen",
    "pause": "pause",
    "insert": "insert",
    "home": "home",
    "end": "end",
    "page_up": "page_up",
    "page_down": "page_down",
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "f1": "f1",
    "f2": "f2",
    "f3": "f3",
    "f4": "f4",
    "f5": "f5",
    "f6": "f6",
    "f7": "f7",
    "f8": "f8",
    "f9": "f9",
    "f10": "f10",
    "f11": "f11",
    "f12": "f12",
}

# 功能键集合（不可作为普通文本输入的键）
SPECIAL_KEYS: Final[frozenset[str]] = frozenset({
    "ctrl", "alt", "shift", "cmd", "win",
    "enter", "tab", "space", "backspace", "delete",
    "escape", "caps_lock", "num_lock", "scroll_lock",
    "print_screen", "pause", "insert",
    "home", "end", "page_up", "page_down",
    "up", "down", "left", "right",
    "f1", "f2", "f3", "f4", "f5", "f6",
    "f7", "f8", "f9", "f10", "f11", "f12",
})

# ── 鼠标按钮映射 ─────────────────────────────────────
MOUSE_BUTTON_MAP: Final[dict[str, str]] = {
    "left": "left",
    "right": "right",
    "middle": "middle",
    "l": "left",
    "r": "right",
    "m": "middle",
}

# ── 截图相关常量 ─────────────────────────────────────
SCREENSHOT_FILENAME_PREFIX: Final[str] = "screenshot"
SCREENSHOT_MAX_FILE_SIZE_MB: Final[int] = 10

# ── 坐标系统常量 ─────────────────────────────────────
NORMALIZED_MIN: Final[float] = 0.0
NORMALIZED_MAX: Final[float] = 1.0

# ── Windows DPI 常量 ─────────────────────────────────
# Windows 10 1803+ 支持 Per-Monitor DPI Aware V2
DEFAULT_DPI_SCALE: Final[float] = 1.0
DPI_SCALE_PRESETS: Final[dict[int, float]] = {
    100: 1.0,    # 100% 缩放
    125: 1.25,   # 125% 缩放
    150: 1.5,    # 150% 缩放
    175: 1.75,   # 175% 缩放
    200: 2.0,    # 200% 缩放（4K 屏幕常见）
    250: 2.5,    # 250% 缩放
    300: 3.0,    # 300% 缩放
    350: 3.5,    # 350% 缩放
    400: 4.0,    # 400% 缩放
}

# ── System 工具常量 ──────────────────────────────────
SLEEP_MAX_SECONDS: Final[float] = 30.0
PING_DEFAULT_COUNT: Final[int] = 4
PING_TIMEOUT_SECONDS: Final[int] = 10
