"""工具基类 / 工具协议。

定义 MCP 工具函数的类型约束，保证所有 tool 注册函数签名一致。"""

from __future__ import annotations

from typing import Any, Callable, Coroutine, Protocol, runtime_checkable


@runtime_checkable
class ToolFunc(Protocol):
    """MCP 工具函数的协议签名。

    所有通过 @mcp.tool() 注册的异步函数都应符合此协议。
    """

    async def __call__(self, **kwargs: Any) -> str: ...


# 工具注册函数类型：接收 FastMCP 实例和对应 Service，注册所有工具
RegisterFunc = Callable[..., Coroutine[Any, Any, None]]
