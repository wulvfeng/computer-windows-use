"""全局配置。

基于 pydantic-settings，支持从环境变量、.env 文件加载。
所有可配置项集中在此，禁止散落在业务代码中硬编码。"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# 项目根目录
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


class AppSettings(BaseSettings):
    """应用全局配置，环境变量前缀 COMPUTER_MCP_。"""

    model_config = SettingsConfigDict(
        env_prefix="COMPUTER_MCP_",
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── 服务基础 ──────────────────────────────────────
    server_name: str = Field(default="computer-mcp", description="服务名称")
    transport: str = Field(default="stdio", description="传输方式：stdio / sse")
    ai_assistant_name: str = Field(default="AI", description="AI 助手名称，用于浮窗显示，如 Claude、GPT-4o")

    # ── 鼠标 ──────────────────────────────────────────
    mouse_driver: str = Field(default="pynput", description="鼠标驱动：pynput | human_mouse")
    mouse_move_duration_min: float = Field(default=0.3, description="鼠标移动最短时间（秒）")
    mouse_move_duration_max: float = Field(default=0.8, description="鼠标移动最长时间（秒）")
    mouse_click_delay: float = Field(default=0.05, description="鼠标点击延迟（秒）")
    mouse_jitter: float = Field(default=2.0, description="鼠标抖动像素范围")
    mouse_bezier_points: int = Field(default=7, description="贝塞尔曲线控制点数")

    # ── 键盘 ──────────────────────────────────────────
    keyboard_driver: str = Field(default="pynput", description="键盘驱动：pynput | humandriver")
    keyboard_typing_speed_min: float = Field(default=0.05, description="打字最短间隔（秒）")
    keyboard_typing_speed_max: float = Field(default=0.15, description="打字最长间隔（秒）")
    keyboard_typing_variation: float = Field(default=0.3, description="打字速度随机变化系数")
    keyboard_human_like: bool = Field(default=True, description="是否启用拟人化打字")

    # ── 截图 ──────────────────────────────────────────
    screenshot_quality: int = Field(default=85, description="截图 JPEG 质量（PNG 时忽略）")
    screenshot_format: str = Field(default="png", description="截图格式：png | jpeg")
    screenshot_max_width: int = Field(default=1920, description="截图最大宽度，超出时等比缩放")
    screenshot_save_to_file: bool = Field(default=False, description="是否保存截图到文件")
    screenshot_capture_cursor: bool = Field(default=True, description="截图是否包含鼠标光标")

    # ── 安全 ──────────────────────────────────────────
    safe_mode: bool = Field(default=True, description="安全模式开关")
    max_actions_per_session: int = Field(default=200, description="单次会话最大操作次数")
    dangerous_hotkeys_blocked: list[str] = Field(
        default=[
            "alt+f4",
            "ctrl+shift+delete",
            "ctrl+alt+delete",
            "win+l",
            "win+u",
        ],
        description="被拦截的危险快捷键列表",
    )
    emergency_stop_key: str = Field(default="f12", description="紧急停止触发键")

    # ── 窗口 ──────────────────────────────────────────
    window_focus_before_action: bool = Field(default=True, description="操作前是否先聚焦窗口")
    window_raise_on_focus: bool = Field(default=True, description="聚焦时是否提升窗口层级")

    # ── 日志 ──────────────────────────────────────────
    log_level: str = Field(default="INFO", description="日志级别")
    log_file: str = Field(default="computer_mcp.log", description="日志文件路径")
    audit_log_file: str = Field(default="audit.log", description="审计日志文件路径")
    log_console: bool = Field(default=True, description="是否输出到控制台")

    # ── 路径 ──────────────────────────────────────────
    assets_dir: Path = Field(default=PROJECT_ROOT / "assets", description="资源文件根目录")
    screenshots_dir: Path = Field(default=PROJECT_ROOT / "assets" / "screenshots", description="截图存储目录")
    cache_dir: Path = Field(default=PROJECT_ROOT / "assets" / "cache", description="缓存目录")

    # ── Agent（供 MCP Prompts 使用） ──────────────────
    agent_max_steps: int = Field(default=30, description="Agent 最大步数（提示词用）")
    agent_action_delay: float = Field(default=0.5, description="Agent 动作间隔（秒，提示词用）")


# 全局单例，首次 import 时加载
settings = AppSettings()
