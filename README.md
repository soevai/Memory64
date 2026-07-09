# Memory64

一个跑在 Windows 上的 Python 内存读写与绘制模块。支持 64 位 / 32 位进程内存操作、窗口控制、全局热键、D3D 透明绘制 — 全部通过内置 DLL 调用系统 API，无需额外安装驱动。

![Version](https://img.shields.io/badge/version-1.0.3.dev2-orange) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![Platform](https://img.shields.io/badge/platform-Windows-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Status](https://img.shields.io/badge/status-active-success)

## 功能

- 🧠 内存读写 — 支持 64 位 / 32 位进程的整数、浮点、字符串、字节集读写
- 🎯 模块基址 — 通过进程句柄或 PID 获取 64 位 / 32 位程序模块基址
- 🪟 窗口控制 — 查找窗口、显示/隐藏、关闭、移动、抖动、挂起、消息发送
- ⌨️ 热键监听 — 安装键盘钩子，监听全局热键状态
- 🎨 D3D 绘制 — 在目标窗口上透明绘制矩形、线条、圆、文本
- 📦 零依赖 — 纯内置 DLL，不装驱动，pip 即用

## 为什么写这个模块

市面上的内存读写工具要么要装驱动（加载即拉闸），要么只支持 32 位进程。这个模块的目标是：**把 64 位和 32 位支持统一到一个 pip 包里，同时兼容市面上大多数 Python 版本**。

核心逻辑全部封装在内置 DLL 中，Python 侧只做薄层调用。32 位 Python 兼容性最好，64 位也基本能用。没有 driver、没有内核态操作 — 所有功能走用户态 API。如果你只是想快速做点内存读写、画个 ESP 方框，又不想折腾驱动编译和环境配置，这个可能适合你。

## 跑起来

### 1. 安装

```bash
pip install Memory64
```

### 2. 环境建议

- **推荐 32 位 Python 3.x** — 兼容性最佳，能同时操作 32 位和 64 位目标进程
- 64 位 Python 也能用，但部分古老 32 位目标进程可能受限

### 3. 写两行试试

```python
from Memory64.Bin32 import *

hwnd = Openhwnd("notepad.exe")
pid  = GetProcPid("notepad.exe")
mod  = GetModuleAddr64(hwnd, "kernel32.dll")

print(f"PID: {pid}, Handle: {hwnd}, Base: {hex(mod)}")
```

## API 一览

### Memory64.Function — 窗口与系统操作

| 函数 | 说明 |
|------|------|
| `FindWindowPid(className, windowName)` | 通过窗口类名/标题获取窗口句柄、线程句柄、进程 ID |
| `FindProcessPid(name)` | 通过进程名获取 PID |
| `MonitorHotkeys(keyCode)` | 通过按键 ASCII 码监听热键状态 |
| `WindowShake(hwnd)` | 抖动窗口（类似 QQ 窗口抖动） |
| `ShowWindowAsync(hwnd, state)` | 显示或隐藏窗口 |
| `CloseWindow(hwnd)` | 关闭窗口 |
| `GetWindRect(hwnd)` | 获取窗口矩形坐标 |
| `IsWindowVisible(hwnd)` | 判断窗口是否可见 |
| `MoveWindow(hwnd, x, y, w, h)` | 移动窗口 |
| `SetkeyBoHook(callback)` | 安装键盘钩子 |
| `SendMessage(hwnd, msg, wParam, lParam)` | 向窗口发送消息 |
| `UpdateWindow(hwnd)` | 更新窗口 |
| `WindPending(hwnd)` | 挂起窗口 |

### Memory64.Bin32 — 内存读写（64 位 / 32 位）

| 函数 | 说明 |
|------|------|
| `Openhwnd(name)` | 打开进程句柄 |
| `GetProcPid(name)` | 获取进程 PID |
| `GetModuleAddr64(hwnd, moduleName)` | 通过进程句柄获取模块基址 |
| `GetModule2(pid, moduleName)` | 通过 PID 获取模块基址 |
| `ReadMemory64Int(hwnd, addr)` | 读进程内存整数 |
| `WriteMemory64Int(hwnd, addr, value)` | 写进程内存整数 |
| `ReadMemory64Float(hwnd, addr)` | 读进程内存浮点数 |
| `WriteMemory64Float(hwnd, addr, value)` | 写进程内存浮点数 |
| `ReadMemory64Text(hwnd, addr, length)` | 读进程内存字符串 |
| `WriteMemory64Bytes(hwnd, addr, bytesStr, length)` | 写进程内存字节集 |

### Memory64.D3Gui — D3D 透明绘制

| 函数 | 说明 |
|------|------|
| `ExecDraw(hwnd)` | 初始化 D3D 绘制上下文 |
| `startLoop()` | 开始绘制帧 |
| `endLoop()` | 结束绘制帧 |
| `drawText(x, y, text, color)` | 绘制文本 |
| `drawRect(x, y, w, h, thickness, color)` | 绘制矩形框 |
| `drawLine(x1, y1, x2, y2, thickness, color)` | 绘制线条 |
| `drawCircle(x, y, radius, color)` | 绘制圆 |

## 使用示例

### 获取 64 位模块基址

```python
from Memory64.Bin32 import *

hwnd = Openhwnd("Calculator.exe")        # 打开进程句柄
pid  = GetProcPid("Calculator.exe")      # 获取进程 PID

mod1 = GetModuleAddr64(hwnd, "shlwapi.dll")  # 通过进程句柄获取
mod2 = GetModule2(pid, "shlwapi.dll")        # 通过 PID 获取

print(pid, hwnd, hex(mod1), hex(mod2))
```

### 读写 64 位进程内存

```python
from Memory64.Bin32 import *

hwnd = Openhwnd("Calculator.exe")
mod  = GetModuleAddr64(hwnd, "shlwapi.dll")

# 读内存
addr  = ReadMemory64Int(hwnd, 0x7FF8E64CEC48)       # 直接读地址
addr2 = ReadMemory64Int(hwnd, mod + 0x4EC48)        # 模块 + 偏移
print(addr, addr2)

# 写内存
WriteMemory64Int(hwnd, mod + 0x4EC48, 10)             # 写整数
WriteMemory64Float(hwnd, mod + 0x4EC48, 5.261)        # 写浮点
WriteMemory64Bytes(hwnd, 0x7FF77E2BE72E, "11 33 30 32 32 33 35 40 40 58", 10)  # 写字节集
```

### D3D 透明绘制方框

```
用户启动目标进程 → 获取窗口句柄 → 初始化 D3D 绘制
    │
    ▼
while True:
    startLoop()         ← 开始帧
    drawRect(...)       ← 绘制矩形
    drawText(...)       ← 绘制文本
    endLoop()           ← 提交帧
```

```python
from Memory64 import FindWindowPid
import Memory64.D3Gui

hwnd = FindWindowPid(None, "目标窗口标题")[0]   # 获取窗口句柄
draw = Memory64.D3Gui.ExecDraw(hwnd)            # 初始化绘制

while True:
    draw.startLoop()
    draw.drawRect(100, 100, 100, 100, 5, (255, 254, 0))  # 黄色矩形框
    draw.drawText(110, 110, "ESP", (0, 255, 0))          # 绿色文本
    draw.endLoop()
```

## 项目结构

```
Memory64/
├── Memory64/
│   ├── __init__.py
│   ├── Function.py          # 窗口操作 & 热键 & 钩子
│   ├── Bin32.py             # 内存读写 & 模块基址
│   ├── D3Gui.py             # D3D 透明绘制
│   └── Bin32.dll            # 核心 C++ DLL（内存操作）
├── README.md
├── setup.py
├── LICENSE                  # MIT
└── python.svg
```

## 版本记录

| 版本 | 说明 | 状态 |
|------|------|------|
| 1.0.3.dev2 | 修复 Bin32.dll 调用报错，新增 64 位进程读写 | ✅ |
| 1.0.2.dev2 | 修复 Bin32.dll 调用路径错误 | ✅ |
| 1.0.1.dev2 | 修复 D3Gui 绘制报错，更新目录结构与语法 | ✅ |
| 1.0.0.dev2 | 第一版，全是 BUG 😅 | ✅ |

## 常见问题

**import 报 DLL 找不到？** 确认 Python 是 32 位版本。64 位 Python 调用 32 位 DLL 会失败。

**D3Gui 绘制不显示？** 检查目标窗口句柄是否正确。某些窗口有反绘制保护（如 Overlay 检测），绘制可能不生效。

**ReadMemory 返回 0 或报错？** 地址可能无效或进程有保护。先用 `GetModuleAddr64` 确认模块基址正确，再加偏移读。

**为什么推荐 32 位 Python？** Bin32.dll 是 32 位编译的。32 位 Python 原生加载 32 位 DLL，兼容性最好。64 位 Python 需要 WOW64 桥接，部分场景下会有问题。

## 免责声明

本软件开源，仅供学习和研究。

- 禁止用于任何违法违规用途（游戏作弊破坏公平性、盗取他人信息、商业外挂等）
- 对第三方程序进行内存读写可能违反其用户协议，造成的封号/法律后果由使用者自行承担
- 作者不参与任何使用者的商业活动，不承担任何连带责任
- 部署前自己审查代码，根据当地法规调整

不同意以上条款就别用。

## 许可证

MIT License · Copyright (c) 2026 [VoxShadow (发光的神)](https://github.com/soevai)

## 联系

- 哔哩哔哩: [https://space.bilibili.com/84500837](https://space.bilibili.com/84500837)
- 技术交流群: 1029775623
- 个人博客: [https://www.52tt.pro](https://www.52tt.pro)
