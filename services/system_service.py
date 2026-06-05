"""系统服务。

提供系统信息查询、延迟等待、健康检查等业务逻辑。"""

from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

from core.exceptions import ComputerMCPError
from core.result import ToolResult
from tools.system.info import get_system_info
from tools.system.process import find_process, get_system_stats, list_running_processes

if TYPE_CHECKING:
    from core.security import SecurityGuard

# 服务启动时间
_START_TIME: float = time.time()


class SystemService:
    """系统服务 — 提供系统信息和健康检查能力。"""

    def __init__(self, security: SecurityGuard) -> None:
        self._security = security

    async def sleep(self, seconds: float) -> str:
        """等待指定时间。"""
        try:
            # 限制最大等待时间
            seconds = max(0.1, min(seconds, 30.0))
            await asyncio.sleep(seconds)

            result = ToolResult.ok(data={"waited_seconds": seconds})
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def ping(self) -> str:
        """检查服务状态。"""
        try:
            info = get_system_info()
            uptime = time.time() - _START_TIME

            data = {
                "status": "ok",
                "uptime_seconds": round(uptime, 1),
                "action_count": self._security.action_count,
                "remaining_actions": self._security.remaining_actions,
                "version": "0.1.0",
                "safe_mode": self._security.is_safe_mode,
                "system": info,
            }

            result = ToolResult.ok(data=data)
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def list_processes(
        self,
        sort_by: str = "memory",
        limit: int = 30,
        name_filter: str | None = None,
    ) -> str:
        """列出运行中的进程。"""
        try:
            self._security.check_emergency_stop()

            processes = await asyncio.to_thread(
                list_running_processes, sort_by, limit, name_filter,
            )

            self._security.record_action("list_processes", f"sort={sort_by} filter={name_filter}")

            data = {
                "count": len(processes),
                "sort_by": sort_by,
                "processes": processes,
            }

            result = ToolResult.ok(data=data)
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def find_process(self, keyword: str) -> str:
        """查找运行中的进程。"""
        try:
            self._security.check_emergency_stop()

            processes = await asyncio.to_thread(find_process, keyword)

            self._security.record_action("find_process", f"keyword={keyword}")

            data = {
                "keyword": keyword,
                "count": len(processes),
                "processes": processes,
            }

            result = ToolResult.ok(data=data)
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()

    async def get_system_stats(self) -> str:
        """获取系统资源使用率。"""
        try:
            self._security.check_emergency_stop()

            stats = await asyncio.to_thread(get_system_stats)

            result = ToolResult.ok(data=stats)
            return result.to_mcp_response()

        except ComputerMCPError as e:
            return ToolResult.from_exception(e).to_mcp_response()
