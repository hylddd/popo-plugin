#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#

import thread
import time

import datetime
from collections import defaultdict
import functools

import tornado.httpserver
import tornado.ioloop
import tornado.web
from gi.repository import Notify

action_focus='32772'
action_flash='32774'

class Record(object):
    def __init__(self, count, last_action):
        self.count = count
        self.last_action = last_action

Record = functools.partial(Record, 0, action_focus)

db = defaultdict(Record)

CHECK_INTERVAL = 60 # seconds

unread_set = set()
last_notify_time = datetime.datetime(2000, 1, 1)

def popo_notify(content):
    global last_notify_time
    last_notify_time = datetime.datetime.now()
    Hello = Notify.Notification.new("主人，您有了新的泡泡消息", content, "/home/dd/workspace/popo-plugin/avatar.png")
    Hello.show()

def watcher():
    while True:
        time.sleep(2)
        now = datetime.datetime.now()
        if now > last_notify_time + datetime.timedelta(seconds=CHECK_INTERVAL) and len(unread_set) > 0:
            popo_notify("\n".join(unread_set))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        now = datetime.datetime.now()
        title = self.get_argument('title')
        action = self.get_argument('action')
        # print title, action
        record = db[title]

        if action == action_flash:
            if record.last_action != action_flash:
                popo_notify(title)
                self.write(title)
            unread_set.add(title)
        else:
            unread_set.discard(title)
        record.last_action = action


settings = {
    'debug': True,
}

application = tornado.web.Application(
    [(r"/", MainHandler),
     ],
    **settings
)


if __name__ == "__main__":
    try:
        thread.start_new_thread( watcher, () )
    except:
        print "Error: unable to start thread"
    Notify.init("popo")
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(34567)
    tornado.ioloop.IOLoop.instance().start()
