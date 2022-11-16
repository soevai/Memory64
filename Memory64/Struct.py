''' Data Structure '''

import ctypes as _ctype

class RECT(_ctype.Structure):
    _fields_ = [
        ('Left', _ctype.c_long),
        ('Top', _ctype.c_long),
        ('Right', _ctype.c_long),
        ('Bottom', _ctype.c_long)]

class MODULEENTRY32(_ctype.Structure):
    _fields_ = [
        ('dwSize', _ctype.c_long),
        ('th32ModuleID', _ctype.c_long),
        ('th32ProcessID', _ctype.c_long),
        ('GlblcntUsage', _ctype.c_long),
        ('ProccntUsage', _ctype.c_long),
        ('modBaseAddr', _ctype.c_long),
        ('modBaseSize', _ctype.c_long),
        ('hModule', _ctype.c_void_p),
        ('szModule', _ctype.c_char * 256),
        ('szExePath', _ctype.c_char * 260)]

class PROCESS_BASIC_INFORMATION(_ctype.Structure):
    _fields_ = [
        ('ExitStatus', _ctype.c_ulonglong),
        ('PebBaseAddress', _ctype.c_ulonglong),
        ('AffinityMask', _ctype.c_ulonglong),
        ('BasePriority', _ctype.c_ulonglong),
        ('UniqueProcessId', _ctype.c_ulonglong),
        ('InheritedFromUniqueProcessId', _ctype.c_ulonglong)]

class PROCESSENTRY32(_ctype.Structure):
    _fields_ = [
        ('dwSize', _ctype.c_long),
        ('cntUsage', _ctype.c_long),
        ('th32ProcessID', _ctype.c_long),
        ('th32DefaultHeapID', _ctype.c_long),
        ('th32ModuleID', _ctype.c_long),
        ('cntThreads', _ctype.c_long),
        ('th32ParentProcessID', _ctype.c_long),
        ('pcPriClassBase', _ctype.c_long),
        ('dwFlags', _ctype.c_long),
        ('ProcessName', _ctype.c_char * 260)]