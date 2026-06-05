"""AI 操控浮窗。

当 MCP 工具被调用时，在屏幕顶部显示一个浮窗，提示用户 AI 正在操控电脑。
浮窗自动隐藏，支持动画效果。
"""

from __future__ import annotations

import threading
import tkinter as tk
from typing import Optional


class AIOverlay:
    """屏幕顶部浮窗 — 显示 AI 操控状态。

    特性：
    - 半透明深色背景
    - 圆点动画表示活跃状态
    - 自动隐藏（无操作后）
    - 线程安全
    """

    # 浮窗配置
    WIDTH = 320
    HEIGHT = 36
    BG_COLOR = "#1a1a2e"
    TEXT_COLOR = "#e0e0e0"
    DOT_COLORS = ["#00d4ff", "#7b68ee", "#ff6b9d", "#00d4ff"]
    FONT_SIZE = 11
    AUTO_HIDE_SECONDS = 5  # 无操作后自动隐藏的秒数

    def __init__(self, assistant_name: str = "AI") -> None:
        self._assistant_name = assistant_name
        self._root: Optional[tk.Tk] = None
        self._thread: Optional[threading.Thread] = None
        self._visible = False
        self._hide_timer: Optional[threading.Timer] = None
        self._dot_index = 0
        self._animation_id: Optional[str] = None
        self._lock = threading.Lock()
        self._initialized = False

    def _init_root(self) -> None:
        """在后台线程中初始化 tkinter 根窗口。"""
        with self._lock:
            if self._initialized:
                return
            try:
                self._root = tk.Tk()
                self._root.withdraw()  # 先隐藏
                self._root.overrideredirect(True)  # 无边框
                self._root.attributes("-topmost", True)  # 始终置顶
                self._root.attributes("-alpha", 0.92)  # 半透明

                # Windows 特殊设置：穿透点击
                self._root.attributes("-toolwindow", True)

                # 屏幕顶部居中
                screen_w = self._root.winfo_screenwidth()
                x = (screen_w - self.WIDTH) // 2
                self._root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+8")

                # 背景
                self._root.configure(bg=self.BG_COLOR)

                # 内容框架
                frame = tk.Frame(self._root, bg=self.BG_COLOR)
                frame.pack(fill=tk.BOTH, expand=True, padx=10)

                # 动画圆点
                self._dot_label = tk.Label(
                    frame, text="●", font=("Consolas", 14),
                    fg=self.DOT_COLORS[0], bg=self.BG_COLOR,
                )
                self._dot_label.pack(side=tk.LEFT, padx=(0, 8))

                # 文本
                self._text_label = tk.Label(
                    frame,
                    text=f"{self._assistant_name} 正在操控您的电脑",
                    font=("Microsoft YaHei", self.FONT_SIZE),
                    fg=self.TEXT_COLOR, bg=self.BG_COLOR,
                )
                self._text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

                self._initialized = True
            except Exception:
                # tkinter 不可用时静默失败
                self._root = None

    def _animate(self) -> None:
        """动画循环 — 圆点颜色渐变。"""
        if not self._visible or not self._root:
            return
        try:
            self._dot_index = (self._dot_index + 1) % len(self.DOT_COLORS)
            self._dot_label.configure(fg=self.DOT_COLORS[self._dot_index])
            self._animation_id = self._root.after(300, self._animate)
        except Exception:
            pass

    def _schedule_hide(self) -> None:
        """安排自动隐藏。"""
        if self._hide_timer:
            self._hide_timer.cancel()
        self._hide_timer = threading.Timer(self.AUTO_HIDE_SECONDS, self.hide)
        self._hide_timer.daemon = True
        self._hide_timer.start()

    def _ensure_thread(self) -> None:
        """确保 tkinter 运行在独立线程中。"""
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        """tkinter 主循环（运行在独立线程）。"""
        self._init_root()
        if self._root:
            self._root.mainloop()

    def show(self, message: str | None = None) -> None:
        """显示浮窗。

        Args:
            message: 自定义消息，None 则使用默认文本
        """
        self._ensure_thread()

        # 等待初始化完成
        for _ in range(50):
            if self._initialized:
                break
            import time
            time.sleep(0.05)

        if not self._root or not self._initialized:
            return

        try:
            self._root.after(0, self._do_show, message)
        except Exception:
            pass

    def _do_show(self, message: str | None = None) -> None:
        """在 tkinter 线程中执行显示。"""
        with self._lock:
            if not self._root:
                return
            try:
                if message:
                    self._text_label.configure(text=message)
                else:
                    self._text_label.configure(
                        text=f"{self._assistant_name} 正在操控您的电脑"
                    )

                self._root.deiconify()  # 显示窗口
                self._visible = True
                self._dot_index = 0
                self._animate()
                self._schedule_hide()
            except Exception:
                pass

    def hide(self) -> None:
        """隐藏浮窗。"""
        if not self._root or not self._initialized:
            return
        try:
            self._root.after(0, self._do_hide)
        except Exception:
            pass

    def _do_hide(self) -> None:
        """在 tkinter 线程中执行隐藏。"""
        with self._lock:
            if not self._root:
                return
            try:
                self._root.withdraw()
                self._visible = False
                if self._animation_id:
                    self._root.after_cancel(self._animation_id)
                    self._animation_id = None
            except Exception:
                pass

    def update_action(self, action_name: str = "") -> None:
        """有新操作时调用 — 重置自动隐藏计时器并更新文本。"""
        if action_name:
            msg = f"{self._assistant_name} 正在操控: {action_name}"
        else:
            msg = None
        self.show(msg)

    def destroy(self) -> None:
        """销毁浮窗。"""
        if self._hide_timer:
            self._hide_timer.cancel()
        if self._root:
            try:
                self._root.after(0, self._root.destroy)
            except Exception:
                pass
        self._visible = False


# 全局单例
_overlay: Optional[AIOverlay] = None


def init_overlay(assistant_name: str = "AI") -> AIOverlay:
    """初始化全局浮窗。

    Args:
        assistant_name: 助手名称，如 "Claude"、"GPT-4o"、"Gemini"
    """
    global _overlay
    _overlay = AIOverlay(assistant_name)
    return _overlay


def get_overlay() -> Optional[AIOverlay]:
    """获取全局浮窗实例。"""
    return _overlay
