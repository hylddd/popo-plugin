#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#

"""
程序的思路就是通过监控Windows窗口，对比现在和之前有没有新的窗口创建。

如果在新的窗口中有我们所关注的窗口，那么我们就可以通知Linux宿主我们有新的消息了。

当然，这样是有问题，就是在窗口已经打开后，新的消息到来时是无法触发通知的。

TODO:
1. 监控关注窗口的活跃状态
"""

import time
import httplib
import urllib
import traceback
from pprint import pprint
import win32gui
import ctypes
from ctypes import *
import win32con


from ctypes import Structure, sizeof, windll, c_uint, byref
import win32con


LINUX_HOST = "10.0.2.2"
PORT = 34567


class FLASHWINFO(Structure):
    _fields_ = [('cbSize', c_uint),
                ('hwnd', c_uint),
                ('dwFlags', c_uint),
                ('uCount', c_uint),
                ('dwTimeout', c_uint)]


def flash_window(hwnd):
    '''Flash a window with caption and tray.'''
    info = FLASHWINFO(0, hwnd, win32con.FLASHW_ALL | win32con.FLASHW_TIMERNOFG, 0, 0)
    info.cbSize = sizeof(info)
    # return windll.user32.FlashWindowEx(byref(info))
    return windll.user32.FlashWindow(hwnd, 0)


def find_windows(class_name, window_name=None):
    hwnds = []
    try:
        hwnd = win32gui.FindWindow(class_name, window_name)
    except:
        return hwnds
    while hwnd:
        hwnds.append(hwnd)
        hwnd = win32gui.FindWindowEx(None, hwnd, class_name, window_name)
    return hwnds


def print_hwnds(hwnds):
    for hwnd in hwnds:
        print 'hwnd:', hwnd, 'title:', win32gui.GetWindowText(hwnd)


def notify_linux(title):
    return notify_by_web(LINUX_HOST, title, PORT)


def notify_by_web(host, title, port=80):
    """Notify by access http://host/?title=[msg]"""
    try:
        title = title.encode('utf8')
        conn = httplib.HTTPConnection(host, port)
        query = {'title': title, }
        url = '/' + "?" + urllib.urlencode(query)
        conn.request('GET', url)
        return conn.getresponse()
    except:
        traceback.print_exc()


def GetWindowText(hwnd):
    title = win32gui.GetWindowText(hwnd)
    return title.decode("gbk")


def main():
    last_hwnds = set()
    while True:
        class_names = ["SessionForm", "TeamForm", ]
        #window_names = [u"提示",u"兴趣组提示",]
        window_names = []
        allow_team_names = [
            u"某某兴趣小组",
        ]

        print '-' * 40
        hwnds = set()
        for name in class_names:
            hwnds |= set(find_windows(name))
        for name in window_names:
            hwnds |= set(find_windows(None, name.encode('gbk')))

        need_notifies = hwnds - last_hwnds
        print_hwnds(need_notifies)

        for hwnd in last_hwnds:
            if flash_window(hwnd) != 0:
                title = GetWindowText(hwnd)
                rep = notify_linux(title)
                print "flash", rep

        for hwnd in need_notifies:
            title = GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if class_name == "SessionForm":   # for user
                print hwnd, title
                rep = notify_linux(title)
                print rep.read().decode('utf8').encode('gbk')
                continue
            elif class_name == "TeamForm":   # for group
                if title in allow_team_names:
                    print hwnd, title
                    rep = notify_linux(title)
                    print rep.read().decode('utf8').encode('gbk')

        last_hwnds = hwnds

        time.sleep(1)


if __name__ == '__main__':
    main()
