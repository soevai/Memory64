# Python Memory64 Module :ram:

------

## How to Use this Module

- ## 简介

- 这是一个内存模块 最好是用32位版本的Python3 这样兼容些 :

- 哒哒、我会继续更新此模块的，感谢大家的支持 ！！！

- 哔哩哔哩主页: https://space.bilibili.com/84500837

- 许多功能请在模块内查看 这里就不一一赘述了 :baby_bottle:

- 技术交流群: 1029775623

- 个人博客: https://meta.natapp4.cc

------


```python
pip install Memory64 # Windows 安装
```

### Function Module

```python
import Memory64.Function            # 导入 Memory64.Function 模块

Memory64.FindWindowPid()            # 通过窗口类名和名称 取窗口句柄 线程句柄 进程ID
Memory64.Function.FindProcessPid()  # 通过进程名取PID
Memory64.Function.MonitorHotkeys()  # 通过按键Ascii码 监听热键状态
Memory64.Function.WindowShake()     # 抖动窗口 (类似QQ)
Memory64.Function.ShowWindowAsync() # 窗口显示隐藏
Memory64.Function.CloseWindow()     # 关闭窗口
Memory64.Function.GetWindRect()     # 获取窗口矩形
Memory64.Function.IsWindowVisible() # 窗口是否可见
Memory64.Function.MoveWindow()      # 移动窗口
Memory64.Function.SetkeyBoHook()    # 安装键盘钩子
Memory64.Function.SendMessage()     # 窗口发送消息
Memory64.Function.UpdateWindow()    # 更新窗口
Memory64.Function.WindPending()     # 窗口挂起


import Memory64.Bin32               # 导入 Memory64.Function 模块

Memory64.Bin32.Openhwnd()           # 打开进程句柄
Memory64.Bin32.GetProcPid()         # 获取进程PID
Memory64.Bin32.GetModuleAddr64()    # 获取64位 32位进程模块基址
Memory64.Bin32.GetModule2()         # 获取64位 32位进程模块基址
Memory64.Bin32.ReadMemory64Int()    # 读64位 32位进程内存整数
Memory64.Bin32.WriteMemory64Int()   # 写64位 32位进程内存整数
Memory64.Bin32.ReadMemory64Float()  # 读64位 32位进程内存小数
Memory64.Bin32.WriteMemory64Float() # 写64位 32位进程内存小数
Memory64.Bin32.WriteMemory64Bytes() # 写64位 32位进程内存字节集
Memory64.Bin32.ReadMemory64Text()   # 读64位 32位进程内存字符串


import Memory64.D3Gui               # 导入 Memory64.D3Gui 模块

Memory64.D3Gui.ExecDraw()           # 初始化D3Gui
Memory64.D3Gui.drawText()           # 绘制文本
Memory64.D3Gui.drawRect()           # 绘制矩形
Memory64.D3Gui.drawLine()           # 绘制线条
Memory64.D3Gui.drawCircle()         # 绘制圆
Memory64.D3Gui.startLoop()          # 启动绘制段
Memory64.D3Gui.endLoop()            # 结束绘制段
```

| 版本       | 说明                                              | 检查 |
| ---------- | ------------------------------------------------- | ---- |
| 1.0.3.dev2 | 修复Bin32.dll调用报错问题 增加64位进程读写 :wave:             | √    |
| 1.0.2.dev2 | 修复Bin32.dll 调用路径错误问题 :wave:             | √    |
| 1.0.1.dev2 | 修复D3Gui 绘制报错问题 更新目录结构 语法等 :wave: | √    |
| 1.0.0.dev2 | 第一版 全是BUG 滑稽 :ear_of_rice:                 | √    |

---


## 获取64位程序模块基址

```python
from Memory64.Bin32 import *

hwnd = Openhwnd("Calculator.exe")           # 打开进程句柄
pid  = GetProcPid("Calculator.exe")         # 获取进程PID

mod1 = GetModuleAddr64(hwnd, "shlwapi.dll") # 通过进程句柄获取64位程序模块基址
mod2 = GetModule2(pid, "shlwapi.dll")       # 通过进程PID获取64位程序模块基址

print(pid, hwnd, mod1, mod2)                # 输出进程PID, 进程句柄, 输出模块基址
```


## 读写64位进程内存

```python
from Memory64.Bin32 import *

hwnd  = Openhwnd("Calculator.exe")                  # 打开进程句柄
mod1  = GetModuleAddr64(hwnd, "shlwapi.dll")        # 通过进程句柄获取64位程序模块基址
addr  = ReadMemory64Int(hwnd, 0x7FF8E64CEC48)       # 直接读内存地址
addr2 = ReadMemory64Int(hwnd, mod1 + 0x4EC48)       # 配合模块加偏移读内存地址
print(addr, addr2)

WriteMemory64Int(hwnd, mod1 + 0x4EC48, 10)          # 写64位内存整数
WriteMemory64Float(hwnd, mod1 + 0x4EC48, 5.261)     # 写64位内存小数
WriteMemory64Int(hwnd, mod1 + 0x4EC48, 10)          # 写64位内存整数

bytesa = "11 33 30 32 32 33 35 40 40 58"
WriteMemory64Bytes(hwnd, 0x7FF77E2BE72E,bytesa, 10)   # 写64位内存字节集
```

## 透明GUI绘制

```python
from Memory64 import FindWindowPid
import Memory64.D3Gui

hwnd = FindWindowPid(None, "xxx")[0]            # 通过窗口名称取窗口句柄
draw = Memory64.D3Gui.ExecDraw(hwnd)            # 初始化模块

while True:
    draw.startLoop()                             # 开始绘制段
    draw.drawRect(100,100,100,100,5,(255,254,0)) # 绘制矩形
    draw.endLoop()                               # 结束绘制段
```

![](https://raw.githubusercontent.com/2872930558/Memory64/063ca2f162dabc9d713bb93d6abc3c838a3d7479/python.svg)