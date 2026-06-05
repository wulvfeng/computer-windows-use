"""键盘工具注册。

将键盘服务的所有方法注册为 MCP 工具。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

if TYPE_CHECKING:
    from services.keyboard_service import KeyboardService


def register_keyboard_tools(mcp: FastMCP, keyboard_service: KeyboardService) -> None:
    """注册所有键盘相关的 MCP 工具。

    Args:
        mcp: FastMCP 实例
        keyboard_service: 键盘服务实例
    """

    @mcp.tool()
    async def type_text(text: str, interval: float | None = None) -> str:
        """输入文本内容（通过剪贴板粘贴，兼容中英文输入法）。

        无论当前输入法是中文还是英文，均通过剪贴板直接粘贴，
        不会触发输入法候选词，不会被输入法拦截。

        适用场景：在输入框中填写文字、搜索框输入、聊天框发消息等。

        Args:
            text: 要输入的文本（支持中英文混合）
            interval: 保留参数，当前版本忽略
        """
        return await keyboard_service.type_text(text, interval)

    @mcp.tool()
    async def press_key(key: str) -> str:
        """按下单个键并释放（键盘控制，非文本输入）。

        用于操控界面，如 Enter 提交、Tab 切换焦点、Escape 关闭弹窗等。
        不适用于输入文字，输入文字请用 type_text。

        支持：enter, tab, space, backspace, delete, escape, f1~f12, up, down, left, right 等。

        Args:
            key: 按键名称
        """
        return await keyboard_service.press_key(key)

    @mcp.tool()
    async def key_down(key: str) -> str:
        """按下按键（不释放）。

        用于需要按住按键的场景，如游戏中按住方向键。
        需配合 key_up 使用。

        Args:
            key: 按键名称
        """
        return await keyboard_service.key_down(key)

    @mcp.tool()
    async def key_up(key: str) -> str:
        """释放按键。

        配合 key_down 使用，释放之前按住的键。

        Args:
            key: 按键名称
        """
        return await keyboard_service.key_up(key)

    @mcp.tool()
    async def hotkey(keys: list[str], description: str | None = None) -> str:
        """按下组合键（键盘控制，非文本输入）。

        多个按键同时按下，如 Ctrl+C 复制、Ctrl+V 粘贴、Alt+Tab 切换窗口。
        危险快捷键（如 Alt+F4）在安全模式下会被拦截。
        不适用于输入文字，输入文字请用 type_text。

        Args:
            keys: 按键名称列表，如 ["ctrl", "c"]
            description: 组合键用途描述（仅用于日志）
        """
        return await keyboard_service.hotkey(keys, description)
