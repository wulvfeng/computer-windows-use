"""进程查询模块。

使用 psutil 查询 Windows 运行中的进程。
"""

from __future__ import annotations

from typing import TypedDict

import psutil


class ProcessInfo(TypedDict):
    """进程信息。"""
    pid: int
    name: str
    cpu_percent: float
    memory_mb: float
    status: str
    create_time: str


class SystemStats(TypedDict):
    """系统资源信息。"""
    cpu_percent: float
    cpu_count: int
    memory_total_gb: float
    memory_used_gb: float
    memory_percent: float
    disk_total_gb: float
    disk_used_gb: float
    disk_percent: float


def list_running_processes(
    sort_by: str = "memory",
    limit: int = 30,
    name_filter: str | None = None,
) -> list[ProcessInfo]:
    """列出运行中的进程。

    Args:
        sort_by: 排序方式 — memory（内存）/ cpu（CPU）/ name（名称）
        limit: 返回数量上限
        name_filter: 按名称关键词过滤（不区分大小写）

    Returns:
        进程信息列表
    """
    processes: list[ProcessInfo] = []

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status", "create_time"]):
        try:
            info = proc.info
            name = info["name"] or ""

            # 按名称过滤
            if name_filter and name_filter.lower() not in name.lower():
                continue

            # 获取 CPU 占用（非阻塞）
            cpu = proc.cpu_percent(interval=0)

            # 内存（MB）
            mem_bytes = info["memory_info"].rss if info["memory_info"] else 0
            mem_mb = round(mem_bytes / (1024 * 1024), 1)

            # 创建时间
            from datetime import datetime
            create_time = datetime.fromtimestamp(info["create_time"]).strftime("%Y-%m-%d %H:%M") if info["create_time"] else "unknown"

            processes.append(ProcessInfo(
                pid=info["pid"],
                name=name,
                cpu_percent=round(cpu, 1),
                memory_mb=mem_mb,
                status=info["status"] or "unknown",
                create_time=create_time,
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # 排序
    sort_key = {
        "memory": lambda p: p["memory_mb"],
        "cpu": lambda p: p["cpu_percent"],
        "name": lambda p: p["name"].lower(),
    }.get(sort_by, lambda p: p["memory_mb"])

    processes.sort(key=sort_key, reverse=(sort_by != "name"))

    return processes[:limit]


def find_process(keyword: str) -> list[ProcessInfo]:
    """查找包含关键词的进程。

    Args:
        keyword: 搜索关键词（不区分大小写）

    Returns:
        匹配的进程列表
    """
    return list_running_processes(name_filter=keyword, limit=50, sort_by="memory")


def get_system_stats() -> SystemStats:
    """获取系统资源使用率。"""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count() or 1

    # 内存
    mem = psutil.virtual_memory()
    mem_total = round(mem.total / (1024 ** 3), 2)
    mem_used = round(mem.used / (1024 ** 3), 2)

    # 磁盘（C 盘）
    disk = psutil.disk_usage("C:\\")
    disk_total = round(disk.total / (1024 ** 3), 2)
    disk_used = round(disk.used / (1024 ** 3), 2)

    return SystemStats(
        cpu_percent=cpu_percent,
        cpu_count=cpu_count,
        memory_total_gb=mem_total,
        memory_used_gb=mem_used,
        memory_percent=mem.percent,
        disk_total_gb=disk_total,
        disk_used_gb=disk_used,
        disk_percent=round(disk.percent, 1),
    )
