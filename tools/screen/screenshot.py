"""截图驱动。

使用 mss 进行屏幕截图，支持全屏、单显示器、区域截图。
支持缩放、格式转换、文件保存。"""

from __future__ import annotations

import io
import time
from pathlib import Path
from typing import Optional

import mss
import mss.tools
from PIL import Image

from config.settings import settings
from core.exceptions import MonitorNotFoundError, ScreenshotError


def take_screenshot(
    monitor_index: int = 0,
    max_width: Optional[int] = None,
    fmt: str = "png",
    quality: int = 85,
) -> tuple[bytes, int, int, str]:
    """截取屏幕截图。

    Args:
        monitor_index: 显示器索引，0 表示全部（虚拟屏幕）。
        max_width: 最大宽度，超出时等比缩放。
        fmt: 图片格式 png / jpeg。
        quality: JPEG 质量。

    Returns:
        (图片字节数据, 宽度, 高度, 格式)

    Raises:
        ScreenshotError: 截图失败
        MonitorNotFoundError: 指定的显示器不存在
    """
    try:
        with mss.mss() as sct:
            # 验证显示器索引
            if monitor_index < 0 or monitor_index >= len(sct.monitors) - 1:
                raise MonitorNotFoundError(
                    f"显示器索引 {monitor_index} 不存在，"
                    f"共有 {len(sct.monitors) - 1} 个显示器",
                )

            # monitor_index=0 → 虚拟屏幕（所有显示器）
            monitor = sct.monitors[monitor_index]
            raw = sct.grab(monitor)

            # 转为 PIL Image
            img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
            width, height = img.size

            # 等比缩放
            if max_width and width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
                width, height = img.size

            # 转为字节数据
            buf = io.BytesIO()
            if fmt.lower() == "jpeg":
                img.save(buf, format="JPEG", quality=quality, optimize=True)
            else:
                img.save(buf, format="PNG", optimize=True)
            img_bytes = buf.getvalue()

            return img_bytes, width, height, fmt.lower()

    except (MonitorNotFoundError, ScreenshotError):
        raise
    except Exception as e:
        raise ScreenshotError(f"截图失败: {e}", detail=str(e))


def take_region_screenshot(
    x: int,
    y: int,
    width: int,
    height: int,
    max_width: Optional[int] = None,
    fmt: str = "png",
    quality: int = 85,
) -> tuple[bytes, int, int, str]:
    """截取指定区域的屏幕截图。

    Args:
        x: 区域左上角 X 坐标
        y: 区域左上角 Y 坐标
        width: 区域宽度
        height: 区域高度
        max_width: 最大宽度，超出时等比缩放
        fmt: 图片格式
        quality: JPEG 质量

    Returns:
        (图片字节数据, 实际宽度, 实际高度, 格式)
    """
    if width <= 0 or height <= 0:
        raise ScreenshotError(
            f"区域大小无效: {width}x{height}",
            detail="region_too_small",
        )

    region = {"left": x, "top": y, "width": width, "height": height}

    try:
        with mss.mss() as sct:
            raw = sct.grab(region)
            img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
            actual_w, actual_h = img.size

            # 等比缩放
            if max_width and actual_w > max_width:
                ratio = max_width / actual_w
                new_height = int(actual_h * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
                actual_w, actual_h = img.size

            buf = io.BytesIO()
            if fmt.lower() == "jpeg":
                img.save(buf, format="JPEG", quality=quality, optimize=True)
            else:
                img.save(buf, format="PNG", optimize=True)

            return buf.getvalue(), actual_w, actual_h, fmt.lower()

    except Exception as e:
        raise ScreenshotError(f"区域截图失败: {e}", detail=str(e))


def save_screenshot(
    img_bytes: bytes,
    fmt: str = "png",
    prefix: str = "screenshot",
    directory: Optional[Path] = None,
) -> str:
    """保存截图到文件。

    Args:
        img_bytes: 图片字节数据
        fmt: 图片格式
        prefix: 文件名前缀
        directory: 保存目录

    Returns:
        保存的文件路径
    """
    save_dir = directory or settings.screenshots_dir
    save_dir.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.{fmt}"
    filepath = save_dir / filename
    filepath.write_bytes(img_bytes)

    return str(filepath)
