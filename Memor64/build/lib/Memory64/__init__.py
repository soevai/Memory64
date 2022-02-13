''' Update time > 2022/2/13 '''

from .Memo import SetupProce
from .Bin32 import (
    Protect, ZwOpenProcess, IsWinx64,
    GetModuleAddr64
)
from .Function import (
    GetWindRect, SetkeyBoHook, ShowWindowAsync,
    MonitorHotkeys, FindWindowPid, FindProcessPid,
    MoveWindow, CloseWindow, IsWindowVisible,
    SendMessage, UpdateWindow, WindowShake, WindPending
)

about = '''

# | 作者: 忆梦
# | 维护时间: 2021 <-> 2022
# | 技术交流群: 1029775623
import os
def Thumb(myBox):
    if myBox == "关注":
        os.system("start https://space.bilibili.com/84500837")
        return " (๑ˉ∀ˉ๑) 感谢您的支持~"
    else:
        return " (๑′ㅂ`๑) 感谢您的使用~"
print(Thumb("%s"))

'''.strip()

version = 'Memory64 ver: 1.0.2'
