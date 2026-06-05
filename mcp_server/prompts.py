"""MCP Prompts 定义。

为 MCP 客户端提供预定义的提示词模板，
帮助模型更好地理解和使用电脑操作能力。"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register_all_prompts(mcp: FastMCP) -> None:
    """注册所有 MCP 提示词。

    Args:
        mcp: FastMCP 实例
    """

    @mcp.prompt()
    def computer_use_guide() -> str:
        """电脑操作指南 — 帮助模型理解如何操控 Windows 电脑。"""
        return """# Windows 电脑操作指南

## 推荐工作流

1. **观察**: 首先调用 `observe` 获取当前电脑完整状态
2. **分析**: 根据截图和状态信息理解当前画面
3. **操作**: 根据目标执行鼠标/键盘操作
4. **验证**: 再次 `observe` 确认操作结果

## 坐标系统

- **绝对坐标**: `x=1000, y=500` 表示屏幕像素位置
- **归一化坐标**: `x=0.5, y=0.4, normalized=true` 表示屏幕 50% 宽度、40% 高度处
- 归一化坐标在不同分辨率下都适用，推荐使用

## 常见操作示例

### 打开浏览器
1. `observe` 查看桌面
2. `move_mouse` 到浏览器图标位置
3. `click` 双击打开

### 搜索内容
1. `focus_window` 聚焦浏览器
2. `click` 点击地址栏
3. `hotkey` Ctrl+A 全选
4. `type_text` 输入搜索内容
5. `press_key` enter 搜索

### 复制粘贴
1. `hotkey` Ctrl+C 复制
2. `move_mouse` 移到目标位置
3. `hotkey` Ctrl+V 粘贴

## 安全注意事项

- 危险快捷键（Alt+F4 等）会被拦截
- 每次会话有操作次数限制
- 建议操作间适当 sleep（0.5~2秒）
"""

    @mcp.prompt()
    def observe_and_act(task: str) -> str:
        """观察并执行任务 — 根据具体任务描述，引导模型完成操作。

        Args:
            task: 要完成的任务描述
        """
        return f"""# 任务: {task}

## 执行步骤

1. 调用 `observe` 获取当前电脑完整状态（截图 + 窗口 + 鼠标位置）
2. 仔细观察截图，理解当前屏幕内容
3. 制定操作计划
4. 按步骤执行操作（每次操作后建议 sleep 0.5~1秒）
5. 操作完成后再次 observe 验证结果

## 注意事项

- 每次操作后先观察再进行下一步
- 遇到弹窗、对话框时先截图确认内容
- 如果操作失败，分析原因后重试
- 优先使用归一化坐标（不同分辨率兼容性好）
"""

    @mcp.prompt()
    def debugging_guide() -> str:
        """调试指南 — 帮助模型分析操作失败的原因。"""
        return """# 操作调试指南

当操作未达到预期效果时，按以下步骤排查：

1. **截图确认**: 调用 take_screenshot 查看当前画面
2. **窗口状态**: 调用 active_window 检查目标窗口是否在前台
3. **鼠标位置**: 调用 get_mouse_position 确认鼠标当前在哪
4. **窗口列表**: 调用 list_windows 查看所有可用窗口

## 常见问题

- **点击没反应**: 可能窗口不在前台，先 focus_window
- **文字输入错误**: 确保输入法为英文模式
- **截图为空白**: 可能是 DRM 保护的窗口
- **操作被拒绝**: 可能触发了安全模式限制
"""
