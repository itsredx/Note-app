import win32gui
import win32con
import win32api
import sys

class PowerManagementWindow:
    def __init__(self):
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = 'PowerManagementWindowClass'
        wc.lpfnWndProc = self.wnd_proc
        class_atom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow(
            class_atom,
            'Power Management Window',
            0, 0, 0, 0, 0, 0, 0, None
        )
        print("Listening for power events...")

    def wnd_proc(self, hwnd, msg, w_param, l_param):
        if msg == win32con.WM_POWERBROADCAST:
            if w_param == win32con.PBT_APMRESUMESUSPEND:
                print("System is resuming from sleep.")
                # You can trigger your desired action here
            elif w_param == win32con.PBT_APMSUSPEND:
                print("System is going to sleep.")
        return 0

    def start(self):
        win32gui.PumpMessages()

if __name__ == '__main__':
    pmw = PowerManagementWindow()
    pmw.start()