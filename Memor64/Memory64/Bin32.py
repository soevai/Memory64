''' Bin32 kernel '''

import ctypes as _ctype
import os, shutil
import sys

dllpath = "./Bin32.dll"

def inspect():
    current_path = os.path.abspath(__file__)
    newpath = os.path.join(os.path.dirname(current_path) + os.path.sep + 'Libs/Bin32.dll')
    shutil.copyfile(newpath, dllpath)

def _call_load():
    load_dll = _ctype.CDLL("./Bin32.dll")
    return load_dll

if not os.path.exists(dllpath):
    inspect()
    load_dll = _call_load()
else:
    load_dll = _call_load()

def Protect(pid, bools):
    '''
    :func: 进程保护 (类似360进程防杀)
    :param pid: 进程id
    :param bools: True 开启保护 False 解除保护
    :return:
    '''
    load_dll.Protect(pid, bools)

def ZwOpenProcess(pid, bools):
    '''
    :func: id取进程句柄
    :param pid: 进程id
    :param bools: True ZwOpenProcess强力打开进程 False OpenProcess 打开进程
    :return: 整数
    '''
    return load_dll.ZwOpenProcess(pid, bools)

def IsWinx64(pid):
    '''
    :func: 判断进程是否64位
    :param pid: 进程id
    :return: 整数
    '''
    return load_dll.IsWinx64(pid)

def GetModuleAddr64(pid, moduleName):
    '''
    :func: 驱动获取64位 32位模块基址
    :param pid: 进程id
    :param moduleName: 模块名称 如: dll、exe
    :return: 整数
    '''
    retn = load_dll.GetModuleAddr64(pid, moduleName.encode('gbk'))
    c_longlong = int(_ctype.string_at(retn).decode('gbk'))
    return c_longlong