"""loguru 日志配置。

统一管理控制台输出、文件轮转、审计日志三路日志。
首次 import config.logging 时自动初始化。"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from config.settings import settings, PROJECT_ROOT


def setup_logging() -> None:
    """初始化 loguru 日志系统。

    - 控制台：彩色输出
    - 业务日志：按日轮转，保留 7 天
    - 崩溃日志：ERROR 及以上，单独文件
    - 审计日志：独立文件，记录所有关键操作
    """
    # 移除 loguru 默认处理器
    logger.remove()

    # 日志级别统一转大写
    log_level = settings.log_level.upper()

    # 日志目录（基于项目根目录，确保从任意位置启动都能找到）
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # ── 控制台输出 ────────────────────────────────────
    if settings.log_console:
        logger.add(
            sys.stderr,
            level=log_level,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            ),
            colorize=True,
            backtrace=True,
            diagnose=True,
        )

    # ── 业务日志文件 ──────────────────────────────────
    log_path = log_dir / "computer_mcp.log"
    logger.add(
        str(log_path),
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )

    # ── 崩溃日志（ERROR 及以上，单独文件）─────────────
    crash_path = log_dir / "crash.log"
    logger.add(
        str(crash_path),
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line}\n{message}\n{exception}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )

    # ── 审计日志 ──────────────────────────────────────
    audit_path = log_dir / "audit.log"
    logger.add(
        str(audit_path),
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        filter=lambda record: "[AUDIT]" in record["message"],
    )

    logger.info(f"[系统] 日志系统初始化完成，日志目录: {log_dir}")


# 首次 import 时自动初始化
setup_logging()
