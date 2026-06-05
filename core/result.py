"""统一结果类型。

所有 Service 层方法均返回 ToolResult，保证 MCP 工具层
拿到一致的 success / data / error 结构。"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from core.exceptions import ComputerMCPError


@dataclass
class ToolResult:
    """工具执行结果的统一包装。"""

    success: bool
    data: Any = None
    error: str = ""
    elapsed_ms: float = 0.0
    action_count: int = 0

    # ── 工厂方法 ──────────────────────────────────────

    @classmethod
    def ok(cls, data: Any = None, elapsed_ms: float = 0.0, action_count: int = 0) -> ToolResult:
        """构造成功结果。"""
        return cls(success=True, data=data, elapsed_ms=elapsed_ms, action_count=action_count)

    @classmethod
    def fail(cls, error: str, elapsed_ms: float = 0.0) -> ToolResult:
        """构造失败结果。"""
        return cls(success=False, error=error, elapsed_ms=elapsed_ms)

    @classmethod
    def from_exception(cls, exc: ComputerMCPError, elapsed_ms: float = 0.0) -> ToolResult:
        """从自定义异常构造失败结果。"""
        return cls(success=False, error=str(exc), elapsed_ms=elapsed_ms)

    # ── 计时上下文管理器 ──────────────────────────────

    @classmethod
    def timed(cls) -> _ResultTimer:
        """用作上下文管理器自动计算耗时：

        ```python
        with ToolResult.timed() as timer:
            do_something()
        result = timer.ok(data=some_data)
        ```
        """
        return _ResultTimer()

    # ── 输出 ──────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        """转为可 JSON 序列化的字典。"""
        out: dict[str, Any] = {"success": self.success}
        if self.data is not None:
            out["data"] = self.data
        if self.error:
            out["error"] = self.error
        if self.elapsed_ms > 0:
            out["elapsed_ms"] = round(self.elapsed_ms, 2)
        if self.action_count > 0:
            out["action_count"] = self.action_count
        return out

    def to_mcp_response(self) -> str:
        """转为 MCP 工具返回的纯文本字符串。

        MCP 工具必须返回 str，这里用简洁 JSON 格式。
        """
        import json

        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class _ResultTimer:
    """配合 ToolResult.timed() 使用的内部计时器。"""

    def __init__(self) -> None:
        self._start: float = 0.0
        self._elapsed: float = 0.0

    def __enter__(self) -> _ResultTimer:
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_: Any) -> None:
        self._elapsed = (time.perf_counter() - self._start) * 1000

    @property
    def elapsed_ms(self) -> float:
        return self._elapsed

    def ok(self, data: Any = None, action_count: int = 0) -> ToolResult:
        return ToolResult.ok(data=data, elapsed_ms=self._elapsed, action_count=action_count)

    def fail(self, error: str) -> ToolResult:
        return ToolResult.fail(error=error, elapsed_ms=self._elapsed)
