''' module library '''

import ctypes as libs

class WINDOWS_LIBRARY:
    ntdll = libs.WinDLL("ntdll.dll")
    # kernel32
    resumeThread = libs.windll.kernel32.ResumeThread
    suspendThread = libs.windll.kernel32.SuspendThread
    getModuleHandle = libs.windll.kernel32.GetModuleHandleW
    closeHandle = libs.windll.kernel32.CloseHandle
    openProcess = libs.windll.kernel32.OpenProcess
    process32First = libs.windll.kernel32.Process32First
    readProcessMemory = libs.windll.kernel32.ReadProcessMemory
    writeProcessMemory = libs.windll.kernel32.WriteProcessMemory
    module32Next = libs.windll.kernel32.Module32Next
    process32Next = libs.windll.kernel32.Process32Next
    createToolhelp32 = libs.windll.kernel32.CreateToolhelp32Snapshot
    openThread = libs.windll.kernel32.OpenThread
    # user32
    updateWindow = libs.windll.user32.UpdateWindow
    getWindowTextLength = libs.windll.user32.GetWindowTextLengthA
    sendMessage = libs.windll.user32.SendMessageW
    isWindowVisible = libs.windll.user32.IsWindowVisible
    closeWindow = libs.windll.user32.CloseWindow
    moveWindow = libs.windll.user32.MoveWindow
    getMessageA = libs.windll.user32.GetMessageA
    callNextHookEx = libs.windll.user32.CallNextHookEx
    unhookWindowsHookEx = libs.windll.user32.UnhookWindowsHookEx
    setWindowsHookEx = libs.windll.user32.SetWindowsHookExA
    findWindow = libs.windll.user32.FindWindowW
    setWindowLong = libs.windll.user32.SetWindowLongW
    setWindowPos = libs.windll.user32.SetWindowPos
    getWindowRect = libs.windll.user32.GetWindowRect
    getWindowText = libs.windll.user32.GetWindowTextA
    getAsyncKeyState = libs.windll.user32.GetAsyncKeyState
    showWindowAsync = libs.windll.user32.ShowWindowAsync
    getThreadProcessId = libs.windll.user32.GetWindowThreadProcessId
    setLayeredWindowAttributes = libs.windll.user32.SetLayeredWindowAttributes