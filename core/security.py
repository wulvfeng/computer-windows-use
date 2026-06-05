"""安全模块。

提供动作计数、危险快捷键过滤、坐标边界校验、紧急停止等能力。
SAFE_MODE 开启时所有危险操作均被拦截。"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from core.exceptions import (
    ActionLimitExceededError,
    CoordinateOutOfBoundsError,
    DangerousHotkeyError,
    EmergencyStopError,
)

if TYPE_CHECKING:
    from config.settings import AppSettings

logger = logging.getLogger(__name__)


class SecurityGuard:
    """安全守卫 — 拦截不安全的计算机操作。"""

    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings
        self._action_count: int = 0
        self._start_time: float = time.time()
        self._emergency_stopped: bool = False

    # ── 公开接口 ──────────────────────────────────────

    def check_action_allowed(self) -> None:
        """检查是否还有剩余操作次数配额。超过上限时抛出异常。"""
        if self._action_count >= self._settings.max_actions_per_session:
            raise ActionLimitExceededError(
                limit=self._settings.max_actions_per_session,
                current=self._action_count,
            )

    def record_action(self, action_type: str, detail: str = "") -> None:
        """记录一次操作（计数 + 审计日志 + 浮窗更新）。"""
        self._action_count += 1
        logger.info(
            "[AUDIT] action=%s count=%d detail=%s",
            action_type,
            self._action_count,
            detail,
        )
        # 更新浮窗
        try:
            from core.overlay import get_overlay
            overlay = get_overlay()
            if overlay:
                overlay.update_action(action_type)
        except Exception:
            pass

    def check_hotkey_safe(self, keys: list[str]) -> None:
        """检查快捷键组合是否在黑名单中。

        Args:
            keys: 按键名称列表，如 ["ctrl", "shift", "delete"]

        Raises:
            DangerousHotkeyError: 该快捷键被安全策略拦截
        """
        if not self._settings.safe_mode:
            return

        normalized = "+".join(sorted(k.lower() for k in keys))
        blocked = [
            "+".join(sorted(hk.lower().split("+")))
            for hk in self._settings.dangerous_hotkeys_blocked
        ]

        if normalized in blocked:
            logger.warning("[SECURITY] 危险快捷键被拦截: %s", normalized)
            raise DangerousHotkeyError(
                f"危险快捷键被拦截: {normalized}",
                detail=f"blocked_hotkey={normalized}",
            )

    def check_coordinate_bounds(
        self,
        x: float,
        y: float,
        screen_width: int,
        screen_height: int,
    ) -> None:
        """校验坐标是否在屏幕范围内。

        Raises:
            CoordinateOutOfBoundsError: 坐标越界
        """
        if not (0 <= x <= screen_width and 0 <= y <= screen_height):
            raise CoordinateOutOfBoundsError(
                f"坐标 ({x}, {y}) 超出屏幕边界 ({screen_width}x{screen_height})",
                detail=f"out_of_bounds=({x},{y})",
            )

    def check_emergency_stop(self) -> None:
        """检查紧急停止信号。

        Raises:
            EmergencyStopError: 紧急停止已触发
        """
        if self._emergency_stopped:
            raise EmergencyStopError("鼠标紧急停止已触发", detail="emergency_stop")

    def trigger_emergency_stop(self) -> None:
        """触发紧急停止。"""
        self._emergency_stopped = True
        logger.critical("[SECURITY] 紧急停止已触发！所有鼠标操作将被中断。")

    def reset_emergency_stop(self) -> None:
        """重置紧急停止信号。"""
        self._emergency_stopped = False
        logger.info("[SECURITY] 紧急停止已重置。")

    # ── 查询接口 ──────────────────────────────────────

    @property
    def action_count(self) -> int:
        """当前会话已执行的操作次数。"""
        return self._action_count

    @property
    def remaining_actions(self) -> int:
        """剩余可用操作次数。"""
        return max(0, self._settings.max_actions_per_session - self._action_count)

    @property
    def is_safe_mode(self) -> bool:
        """安全模式是否开启。"""
        return self._settings.safe_mode

    def reset_action_count(self) -> None:
        """重置操作计数（开始新会话时调用）。"""
        self._action_count = 0
        self._start_time = time.time()
        self._emergency_stopped = False
        logger.info("[SECURITY] 操作计数已重置。")

    def get_stats(self) -> dict[str, object]:
        """返回当前安全模块统计信息。"""
        return {
            "safe_mode": self.is_safe_mode,
            "action_count": self._action_count,
            "remaining_actions": self.remaining_actions,
            "emergency_stopped": self._emergency_stopped,
            "elapsed_seconds": round(time.time() - self._start_time, 1),
        }
