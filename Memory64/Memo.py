from .ModLib import WINDOWS_LIBRARY
from .Function import init_Library
from .const import (
    PROCESS_ALL_ACCESS, TH32CS_SNAPMODULE
)
from .Struct import (
    MODULEENTRY32, PROCESS_BASIC_INFORMATION
)
import ctypes as _ctypes

class SetupProce(object):
    def __init__(self, ProcPid) -> None:
        '''
        :func: 设置进程
        :param ProcPid: 进程id
        :return:
        '''
        if ProcPid:
            self.openProcess(ProcPid)

    def openProcess(self, ProcPid):
        self.ProcPid = ProcPid
        self.hProcess = init_Library.openProcess(PROCESS_ALL_ACCESS, 0, ProcPid)

    def memoryIr(self, addr, size=4):
        addr = _ctypes.c_ulonglong(addr)
        retn = _ctypes.c_ulonglong()
        BufferLength = _ctypes.c_ulonglong(size)
        init_Library.ntdll.NtWow64ReadVirtualMemory64(self.hProcess, addr, _ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def memoryWr(self, addr, n, length):
        addr = _ctypes.c_ulonglong(addr)
        retn = _ctypes.c_wchar_p('0' * length)
        BufferLength = _ctypes.c_ulonglong(n)
        init_Library.ntdll.NtWow64ReadVirtualMemory64(int(self.hProcess), addr, retn, BufferLength, 0)
        return retn.value

    def GetBaseAddr(self, moduleName):
        '''
        :func: 用于获取64位32位应用程序模块地址
        :param ModuleName: 模块名称 如: dll、exe
        :return: 整数
        '''
        mod32 = MODULEENTRY32()
        mod32.dwSize = _ctypes.sizeof(MODULEENTRY32)
        hModuleSnap = init_Library.createToolhelp32(TH32CS_SNAPMODULE[0], self.ProcPid)
        if hModuleSnap != -1:
            while True:
                init_Library.module32Next(hModuleSnap, _ctypes.pointer(mod32))
                if mod32.szModule.decode("gbk") == moduleName:
                    init_Library.closeHandle(hModuleSnap)
                    return mod32.modBaseAddr
        else:
            NumberOfBytesRead = _ctypes.c_ulong()
            Buffer = PROCESS_BASIC_INFORMATION()
            Size = _ctypes.c_ulong(48)
            name_len = len(moduleName)
            init_Library.ntdll.NtWow64QueryInformationProcess64(int(self.hProcess), 0,
            _ctypes.byref(Buffer), Size,_ctypes.byref(NumberOfBytesRead))
            ret = self.memoryIr(Buffer.PebBaseAddress + 24, 8)
            ret = self.memoryIr(ret + 24, 8)
            for _ in range(100000):
                modulehandle = self.memoryIr(ret + 48, 8)
                if modulehandle == 0:
                    return 'Module Error -1'
                nameaddr = self.memoryIr(ret + 96, 8)
                name = self.memoryWr(nameaddr, name_len * 2 + 1, name_len)
                if name == moduleName:
                    return modulehandle
                ret = self.memoryIr(ret + 8, 8)

    def ReadMemory(self, addr, size=4):
        '''
        :func: 读内存整数 支持 32位 64位程序
        :param addr: 内存地址
        :param size: 类型大小
        :return: 整数
        '''
        addr_cint = _ctypes.c_int(addr)
        retn = _ctypes.c_ulonglong()
        BufferLength = _ctypes.c_int(size)
        init_Library.readProcessMemory(int(self.hProcess),
        addr_cint, _ctypes.byref(retn), BufferLength, 0)
        if not retn.value:
            addr_ulong = _ctypes.c_ulonglong(addr)
            BufferLength = _ctypes.c_ulonglong(size)
            init_Library.ntdll.NtWow64ReadVirtualMemory64(self.hProcess,
            addr_ulong, _ctypes.byref(retn), BufferLength, 0)
        return retn.value


    def ReadMemory_float(self, addr, size=4):
        '''
        :func: 读内存浮点数 支持 32位 64位程序
        :param addr: 内存地址
        :param size: 类型大小
        :return: 浮点数
        '''
        addr_int = _ctypes.c_int(addr)
        retn = _ctypes.c_float()
        BufferLength = _ctypes.c_int(size)
        init_Library.readProcessMemory(int(self.hProcess),
        addr_int, _ctypes.byref(retn), BufferLength, 0)
        if not retn.value:
            addr_ulong = _ctypes.c_ulonglong(addr)
            BufferLength = _ctypes.c_ulonglong(size)
            init_Library.ntdll.NtWow64ReadVirtualMemory64(self.hProcess,
            addr_ulong, _ctypes.byref(retn), BufferLength,0)
        return retn.value

    def ReadMemory_double(self, addr, size=8):
        '''
        :func: 读内存双精度浮点数 支持 32位 64位程序
        :param addr: 内存地址
        :param size: 类型大小
        :return: 双精度
        '''
        addr_int = _ctypes.c_int(addr)
        retn = _ctypes.c_double()
        BufferLength = _ctypes.c_int(size)
        init_Library.readProcessMemory(int(self.hProcess),
        addr_int, _ctypes.byref(retn), BufferLength, 0)
        if not retn.value:
            addr_ulong = _ctypes.c_ulonglong(addr)
            BufferLength = _ctypes.c_ulonglong(size)
            init_Library.ntdll.NtWow64ReadVirtualMemory64(self.hProcess,
            addr_ulong, _ctypes.byref(retn), BufferLength,0)
        return retn.value

    def ReadMemory_byte(self, addr, size=1):
        '''
        :func: 读内存字节 支持 32位 64位程序
        :param addr: 内存地址
        :param size: 类型大小
        :return: 字节
        '''
        addr_int = _ctypes.c_int(addr)
        retn = _ctypes.c_byte()
        BufferLength = _ctypes.c_int(size)
        init_Library.readProcessMemory(int(self.hProcess),
        addr_int, _ctypes.byref(retn), BufferLength, 0)
        if not retn.value:
            addr_ulong = _ctypes.c_ulonglong(addr)
            BufferLength = _ctypes.c_ulonglong(size)
            init_Library.ntdll.NtWow64ReadVirtualMemory64(self.hProcess,
            addr_ulong, _ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def ReadMemory_bytes(self, address, byte):
        '''
        :func: 读内存字节集 支持 32位程序
        :param address: 内存地址
        :param byte: 字节大小
        :return: 字节
        '''
        c_bytes = _ctypes.c_size_t()
        retn = _ctypes.create_string_buffer(byte)
        init_Library.readProcessMemory(self.hProcess, _ctypes.c_void_p(address),
        _ctypes.byref(retn), byte,_ctypes.byref(c_bytes))
        return retn.raw

    def WriteMemory(self, addr, var, size=4):
        '''
        :func: 写内存整数 支持 32位 64位程序
        :param addr: 内存地址
        :param var: 写入的数值
        :param size: 类型大小
        :return: 逻辑
        '''
        addr_cint = _ctypes.c_int(addr)
        retn = _ctypes.c_ulonglong(var)
        BufferLength = _ctypes.c_int(size)
        rest = init_Library.writeProcessMemory(self.hProcess,
        addr_cint, _ctypes.byref(retn), BufferLength, 0)
        print(rest)
        if not rest:
            addr_ulong = _ctypes.c_ulonglong(addr)
            BufferLength = _ctypes.c_ulonglong(size)
            rest = init_Library.ntdll.NtWow64WriteVirtualMemory64(self.hProcess,
            addr_ulong, _ctypes.byref(retn), BufferLength, 0)
        return rest


    def WriteMemory_float(self, addr, var, size=4):
        '''
        :func: 写内存浮点数 支持 32位 64位程序
        :param addr: 内存地址
        :param var: 写入的数值
        :param size: 类型大小
        :return: 逻辑
        '''
        addr_cint = _ctypes.c_int(addr)
        retn = _ctypes.c_float(var)
        BufferLength = _ctypes.c_int(size)
        rest = init_Library.writeProcessMemory(int(self.hProcess),
        addr_cint, _ctypes.byref(retn), BufferLength, 0)
        if not rest:
            addr_ulong = _ctypes.c_ulonglong(addr)
            BufferLength = _ctypes.c_ulonglong(size)
            rest = init_Library.ntdll.NtWow64WriteVirtualMemory64(self.hProcess,
            addr_ulong, _ctypes.byref(retn), BufferLength, 0)
        return rest


    def WriteMemory_double(self, addr,var, size=8):
        '''
        :func: 写内存双精度 支持 32位 64位程序
        :param addr: 内存地址
        :param var: 写入的数值
        :param size: 类型大小
        :return: 逻辑
        '''
        addr_cint = _ctypes.c_int(addr)
        retn = _ctypes.c_double(var)
        BufferLength = _ctypes.c_int(size)
        rest = init_Library.writeProcessMemory(int(self.hProcess),
        addr_cint, _ctypes.byref(retn), BufferLength, 0)
        if not rest:
            addr_ulong = _ctypes.c_ulonglong(addr)
            BufferLength = _ctypes.c_ulonglong(size)
            rest = init_Library.ntdll.NtWow64WriteVirtualMemory64(self.hProcess,
            addr_ulong, _ctypes.byref(retn), BufferLength, 0)
        return rest


    def WriteMemory_byte(self,addr,var, size=1):
        '''
        :func: 写内存字节 支持 32位 64位程序
        :param addr: 内存地址
        :param var: 写入的数值
        :param size: 类型大小
        :return: 逻辑
        '''
        addr_cint = _ctypes.c_int(addr)
        retn = _ctypes.c_byte(var)
        BufferLength = _ctypes.c_int(size)
        rest = init_Library.writeProcessMemory(int(self.hProcess),
        addr_cint, _ctypes.byref(retn), BufferLength, 0)
        if not rest:
            addr_ulong = _ctypes.c_ulonglong(addr)
            BufferLength = _ctypes.c_ulonglong(size)
            rest = init_Library.ntdll.NtWow64WriteVirtualMemory64(self.hProcess,
            addr_ulong, _ctypes.byref(retn), BufferLength, 0)
        return rest

    def WriteMemory_bytes(self,addr, var, length):
        '''
        :func: 写字节集 支持 32位程序
        :param addr: 内存地址
        :param var: 要写入的字节
        :param length: 写入长度
        :return: 逻辑
        '''
        target = _ctypes.cast(addr, _ctypes.c_char_p)
        return init_Library.writeProcessMemory(self.hProcess,
        target, bytes(bytearray.fromhex(var)), length, 0)