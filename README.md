popo-plugin
===========

Python实现的网易泡泡外挂，用于通知虚拟机外的Linux



## 使用方法

在Linux宿主机中运行

    $ python notifier.py

在Windows虚拟机中

1. 安装[Python2.7](http://www.python.org/ftp/python/2.7.5/python-2.7.5.msi)

2. 安装Dependency目录下的AutoHotKey.exe。或者安装[官网](http://www.autohotkey.com/)最新版本。

3. 修改win-notify.py文件，将LINUX_HOST后的ip地址改为你本机linux的ip地址。

4. 修改AutoHotKey.ahk和ListWindows.ahk里面的win-notify.py的路径。

5. 将AutoHotKey.ahk & ListWindows.ahk载入到AutoHotKey中，并让AutoHotKey开机自动运行。


## Tips
Linux下的依赖项: libnotify, python-gobject


## Change Log

### 2014-5-19
修改提醒方案：有新消息到达时立即提醒；定期检查是否有未读消息，有则提醒。

### 2013-12-13
加上了静默时间，在制定时间内，提醒过的消息不再提醒。一是可以避免消息疯狂弹出，另外可以减少自己被打扰的频率。

### 2013-08-04
配合AutoHotKey使用，抛弃了以前的大部分方案。Windows部分主要由AutoHotKey处理。
