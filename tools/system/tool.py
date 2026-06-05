"""系统工具注册。

将系统服务的所有方法注册为 MCP 工具。"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

if TYPE_CHECKING:
    from services.system_service import SystemService

# 服务启动时间
_START_TIME: float = time.time()


def register_system_tools(mcp: FastMCP, system_service: SystemService) -> None:
    """注册所有系统相关的 MCP 工具。

    Args:
        mcp: FastMCP 实例
        system_service: 系统服务实例
    """

    @mcp.tool()
    async def sleep(seconds: float) -> str:
        """等待指定时间。

        在连续操作之间插入延迟，避免操作过快导致界面来不及响应。

        Args:
            seconds: 等待秒数（建议 0.5~3.0）
        """
        return await system_service.sleep(seconds)

    @mcp.tool()
    async def ping() -> str:
        """检查 MCP 服务状态。

        返回服务运行状态、已运行时间、累计操作次数、版本号。
        """
        return await system_service.ping()

    @mcp.tool()
    async def list_processes(
        sort_by: str = "memory",
        limit: int = 30,
        name_filter: str | None = None,
    ) -> str:
        """列出当前运行中的进程。

        返回进程名称、PID、CPU 使用率、内存占用等信息。

        Args:
            sort_by: 排序方式 — memory（按内存）/ cpu（按CPU）/ name（按名称）
            limit: 返回数量上限，默认 30
            name_filter: 按名称关键词过滤，如 "chrome" 只看 Chrome 相关进程
        """
        return await system_service.list_processes(sort_by, limit, name_filter)

    @mcp.tool()
    async def find_process(keyword: str) -> str:
        """查找某个应用是否在运行。

        按关键词搜索进程名称（不区分大小写）。

        Args:
            keyword: 搜索关键词，如 "chrome"、"wechat"、"notepad"
        """
        return await system_service.find_process(keyword)

    @mcp.tool()
    async def get_system_stats() -> str:
        """获取系统资源使用率。

        返回 CPU 使用率、内存使用量、磁盘使用量等信息。
        """
        return await system_service.get_system_stats()
