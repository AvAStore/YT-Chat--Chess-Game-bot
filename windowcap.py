import numpy as np
import win32gui,win32ui,win32con
import time

class windowCapture:
    w=0
    h=0
    hwnd=None
    cropped_x=0
    cropped_y=0
    offset_x=0
    offset_y=0
    def __init__(self,window_name):
        self.hwnd=win32gui.FindWindow(None,window_name)
        if not self.hwnd:
            raise Exception('Window not Found: {}'.format(window_name))
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w=window_rect[2]-window_rect[0]
        self.h=window_rect[3]-window_rect[1]

        border_pixels=0
        titlebar_pixels=32
        self.w=self.w-(border_pixels*2)
        self.h=self.h-titlebar_pixels-border_pixels

        self.cropped_x=border_pixels
        self.cropped_y=titlebar_pixels

        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

        self.send_x=window_rect[0]
        self.send_y=window_rect[1]

    def get_screenshot(self):
        
        wDC=win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitmap=win32ui.CreateBitmap()
        dataBitmap.CreateCompatibleBitmap(dcObj,self.w,self.h)
        cDC.SelectObject(dataBitmap)
        cDC.BitBlt((0,0),(self.w,self.h),dcObj,(self.cropped_x,self.cropped_y),win32con.SRCCOPY)

        signedIntsArray=dataBitmap.GetBitmapBits(True)
        img=np.fromstring(signedIntsArray,dtype='uint8')
        img.shape=(self.h,self.w,4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd,wDC)
        win32gui.DeleteObject(dataBitmap.GetHandle())

        img=img[...,:3]
        return img,self.offset_x,self.offset_y

    def activatewin(self):
        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(0.1)

    def list_window_names(self):
        def winEnumHandler(hwnd,ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd),win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler,None)

    def get_screen_position(self,pos):
        return (pos[0]+self.offset_x,pos[1]+self.offset_)
