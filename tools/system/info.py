"""系统信息驱动。

获取操作系统、硬件、Python 等系统信息。
使用 psutil 和 ctypes 获取系统级信息。"""

from __future__ import annotations

import os
import platform
import sys
from typing import Any

import psutil

from tools.screen.monitor import get_dpi_scale, get_primary_monitor


def get_system_info() -> dict[str, Any]:
    """获取系统基本信息。

    Returns:
        系统信息字典。
    """
    monitor = get_primary_monitor()
    dpi = get_dpi_scale()

    # 内存信息
    mem = psutil.virtual_memory()

    return {
        "os_name": platform.system(),
        "os_version": platform.version(),
        "hostname": platform.node(),
        "username": os.getlogin() if hasattr(os, "getlogin") else os.environ.get("USERNAME", "unknown"),
        "python_version": sys.version.split()[0],
        "screen_width": int(monitor["width"]),
        "screen_height": int(monitor["height"]),
        "dpi_scale": dpi,
        "cpu_count": psutil.cpu_count() or 1,
        "memory_total_gb": round(mem.total / (1024 ** 3), 2),
    }
