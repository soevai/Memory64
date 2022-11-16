''' Bin32 kernel '''

import ctypes as _ctype
import os, shutil, platform

if platform.architecture()[0] != "32bit":
    print("模块不兼容64位Python")
    os._exit(0)

dll_path = "./Bin32.dll"

def inspect():
    current_path = os.path.abspath(__file__)
    newpath = os.path.join(os.path.dirname(current_path) + os.path.sep + 'Libs/Bin32.dll')
    shutil.copyfile(newpath, dll_path)

if not os.path.exists(dll_path):
    inspect()
load_dll = _ctype.CDLL(dll_path)

def Openhwnd(hwnd):
    '''
    :func: 取进程句柄
    :param hwnd: 进程名称
    :return: 整数
    '''
    return load_dll.openhwnd(hwnd.encode("gbk"))

def GetProcPid(name):
    '''
    :func: 取进程PID
    :param name: 进程名称
    :return: 整数
    '''
    return load_dll.Get_pid(name.encode("gbk"))

def GetModuleAddr64(hwnd, moduleName):
    '''
    :func: 取64位 32位模块基址
    :param hwnd: 进程句柄
    :param moduleName: 模块名称 如: dll、exe
    :return: 整数
    '''
    retn = load_dll.GetModuleAddr64(hwnd, moduleName.encode('gbk'))
    c_longlong = int(_ctype.string_at(retn).decode('gbk'), 16)
    return c_longlong

def GetModule2(pid, moduleName):
    '''
    :func: 取64位 32位模块基址
    :param hwnd: 进程PID
    :param moduleName: 模块名称 如: dll、exe
    :return: 整数
    '''
    return int(_ctype.string_at(load_dll.GetModule2(pid, moduleName.encode('gbk'))))

def ReadMemory64Int(hwnd, addr):
    '''
    :func: 读64 32位内存整数
    :param hwnd: 进程句柄
    :param addr: 内存地址
    :return: 整数
    '''
    return load_dll.read_memory64_int(hwnd, str(hex(addr)[2:]).encode('gbk'))

def WriteMemory64Int(hwnd, addr, var):
    '''
    :func: 写64 32位内存整数
    :param hwnd: 进程句柄
    :param addr: 内存地址
    :return: 整数
    '''
    return load_dll.write_memory64_int(hwnd, str(hex(addr)[2:]).encode('gbk'), var)

def ReadMemory64Float(hwnd, addr):
    '''
    :func: 读64 32位内存小数
    :param hwnd: 进程句柄
    :param addr: 内存地址
    :return: 小数
    '''
    return float(_ctype.string_at(load_dll.read_memory64_float(hwnd, str(hex(addr)[2:]).encode('gbk'))))

def WriteMemory64Float(hwnd, addr, var):
    '''
    :func: 写64 32位内存小数
    :param hwnd: 进程句柄
    :param addr: 内存地址
    :return: 逻辑
    '''
    return load_dll.write_memory64_float(hwnd, str(hex(addr)[2:]).encode('gbk'), str(var).encode('gbk'))

def WriteMemory64Bytes(hwnd, addr, var, length):
    '''
    :func: 写64 32位内存字节集
    :param hwnd: 进程句柄
    :param addr: 内存地址
    :return: 逻辑
    '''
    return load_dll.write_memory64_bytes(hwnd, str(hex(addr)[2:]).encode('gbk'), var.encode('gbk'), length)

def ReadMemory64Text(hwnd, addr,  length):
    '''
    :func: 读64 32位内存字符串
    :param hwnd: 进程句柄
    :param addr: 内存地址
    :return: 字符串
    '''
    return _ctype.string_at(load_dll.read_memory64_bytes(hwnd, str(hex(addr)[2:]).encode('gbk'), length)).decode("gbk")