"""pynput 键盘驱动。

使用 pynput 库实现键盘操作。
中文输入通过剪贴板粘贴实现，绕过 IME 限制。
"""

from __future__ import annotations

import random
import time

from pynput.keyboard import Controller, Key

from config.constants import KEY_NAME_MAP, SPECIAL_KEYS
from tools.keyboard.driver import KeyboardDriver


# pynput Key 属性名映射
_PYNPUT_KEY_MAP: dict[str, Key] = {
    "enter": Key.enter,
    "return": Key.enter,
    "tab": Key.tab,
    "space": Key.space,
    "backspace": Key.backspace,
    "delete": Key.delete,
    "escape": Key.esc,
    "esc": Key.esc,
    "ctrl": Key.ctrl_l,
    "ctrl_l": Key.ctrl_l,
    "ctrl_r": Key.ctrl_r,
    "alt": Key.alt_l,
    "alt_l": Key.alt_l,
    "alt_gr": Key.alt_gr,
    "shift": Key.shift_l,
    "shift_l": Key.shift_l,
    "shift_r": Key.shift_r,
    "cmd": Key.cmd_l,
    "cmd_l": Key.cmd_l,
    "cmd_r": Key.cmd_r,
    "win": Key.cmd_l,
    "win_l": Key.cmd_l,
    "win_r": Key.cmd_r,
    "caps_lock": Key.caps_lock,
    "num_lock": Key.num_lock,
    "scroll_lock": Key.scroll_lock,
    "print_screen": Key.print_screen,
    "pause": Key.pause,
    "insert": Key.insert,
    "home": Key.home,
    "end": Key.end,
    "page_up": Key.page_up,
    "page_down": Key.page_down,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,
}


class PynputKeyboardDriver(KeyboardDriver):
    """基于 pynput 的键盘驱动。"""

    def __init__(self) -> None:
        super().__init__()
        self._keyboard = Controller()

    def _resolve_key(self, key_name: str):  # type: ignore[no-untyped-def]
        """将用户键名转为 pynput Key 对象或字符。"""
        normalized = KEY_NAME_MAP.get(key_name.lower(), key_name.lower())
        if normalized in _PYNPUT_KEY_MAP:
            return _PYNPUT_KEY_MAP[normalized]
        # 如果是单个字符，直接返回
        if len(key_name) == 1:
            return key_name
        raise ValueError(f"无法识别的按键: {key_name}")

    def type_text(self, text: str, interval: float | None = None) -> None:
        """输入文本。

        全部通过剪贴板粘贴，彻底绕过输入法（IME）。
        无论中英文，均不触发 IME 候选词，直接粘贴到目标输入框。
        """
        if not text:
            return

        # 整段文本一次性粘贴（效率最高，无 IME 干扰）
        self._clipboard_paste(text)

    def _clipboard_paste(self, text: str) -> None:
        """通过剪贴板粘贴文本（支持中文等非 ASCII 字符）。

        流程：保存旧剪贴板 → 写入文本 → Ctrl+V 粘贴 → 恢复旧剪贴板。
        """
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        CF_UNICODETEXT = 13
        GMEM_MOVEABLE = 0x0002

        # 保存当前剪贴板内容
        old_data = None
        if user32.OpenClipboard(0):
            try:
                h = user32.GetClipboardData(CF_UNICODETEXT)
                if h:
                    old_ptr = kernel32.GlobalLock(h)
                    if old_ptr:
                        old_data = ctypes.c_wchar_p(old_ptr).value
                        kernel32.GlobalUnlock(h)
            except Exception:
                pass

            # 清空剪贴板
            user32.EmptyClipboard()

            # 写入新文本
            text_encoded = text + "\0"
            buf = ctypes.create_unicode_buffer(text_encoded)
            h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(text_encoded) * 2)
            if h_mem:
                ptr = kernel32.GlobalLock(h_mem)
                if ptr:
                    ctypes.memmove(ptr, ctypes.addressof(buf), len(text_encoded) * 2)
                    kernel32.GlobalUnlock(h_mem)
                user32.SetClipboardData(CF_UNICODETEXT, h_mem)

            user32.CloseClipboard()

        # Ctrl+V 粘贴
        self._keyboard.press(Key.ctrl_l)
        self._keyboard.press("v")
        self._keyboard.release("v")
        self._keyboard.release(Key.ctrl_l)
        time.sleep(0.15)

        # 恢复旧剪贴板内容
        if old_data and user32.OpenClipboard(0):
            try:
                user32.EmptyClipboard()
                buf = ctypes.create_unicode_buffer(old_data + "\0")
                h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(old_data + "\0") * 2)
                if h_mem:
                    ptr = kernel32.GlobalLock(h_mem)
                    if ptr:
                        ctypes.memmove(ptr, ctypes.addressof(buf), len(old_data + "\0") * 2)
                        kernel32.GlobalUnlock(h_mem)
                    user32.SetClipboardData(CF_UNICODETEXT, h_mem)
            except Exception:
                pass
            user32.CloseClipboard()

    def press_key(self, key: str) -> None:
        """按下并释放一个键。"""
        resolved = self._resolve_key(key)
        self._keyboard.press(resolved)
        time.sleep(0.02)
        self._keyboard.release(resolved)

    def key_down(self, key: str) -> None:
        """按下按键（不释放）。"""
        resolved = self._resolve_key(key)
        self._keyboard.press(resolved)

    def key_up(self, key: str) -> None:
        """释放按键。"""
        resolved = self._resolve_key(key)
        self._keyboard.release(resolved)

    def hotkey(self, keys: list[str]) -> None:
        """按下组合键。先按住所有键，再按相反顺序释放。"""
        resolved_keys = [self._resolve_key(k) for k in keys]
        for k in resolved_keys:
            self._keyboard.press(k)
            time.sleep(0.02)
        for k in reversed(resolved_keys):
            self._keyboard.release(k)
            time.sleep(0.02)
