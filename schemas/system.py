"""系统信息的数据模型。

定义系统信息查询结果等 Pydantic 模型。"""

from __future__ import annotations

from pydantic import BaseModel, Field


class SystemInfo(BaseModel):
    """系统基本信息。"""

    os_name: str = Field(description="操作系统名称")
    os_version: str = Field(description="操作系统版本")
    hostname: str = Field(description="计算机名")
    username: str = Field(description="当前用户名")
    python_version: str = Field(description="Python 版本")
    screen_width: int = Field(description="主屏幕宽度")
    screen_height: int = Field(description="主屏幕高度")
    dpi_scale: float = Field(description="DPI 缩放比例")
    cpu_count: int = Field(description="CPU 核心数")
    memory_total_gb: float = Field(description="总内存（GB）")


class PingResult(BaseModel):
    """Ping 响应。"""

    status: str = Field(default="ok", description="服务状态")
    uptime_seconds: float = Field(description="服务运行时间（秒）")
    action_count: int = Field(description="累计操作次数")
    version: str = Field(description="服务版本号")
