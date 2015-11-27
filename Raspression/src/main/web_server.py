from threading import Thread

__author__ = 'Barri Mason'

import web
import sys

rasp_server = None


class WebServer(Thread):

    app = None

    urls = (
        "/value", "Values",
        "/value/([0-9]*)", "Value",

        "/min/([0-9]*)", "Min",
        "/min/([0-9]*)/([0-9]*)", "SetMin",

        "/max/([0-9]*)", "Max",
        "/max/([0-9]*)/([0-9]*)", "SetMax",

        "/def/([0-9]*)", "Def",
        "/def/([0-9]*)/([0-9]*)", "SetDef",

        "/cc/([0-9]*)", "Cc",
        "/cc/([0-9]*)/([0-9]*)", "SetCc",

        "/sens/([0-9]*)", "Sens",
        "/sens/([0-9]*)/([0-9]*)", "SetSens",

        "/time/([0-9]*)", "Time",
        "/time/([0-9]*)/([0-9]*)", "SetTime",

        "/save", "Save",

        "/shutdown", "Shutdown"
    )

    def __init__(self, rs):
        super(WebServer, self).__init__()
        global rasp_server
        rasp_server = rs

    def start(self):
        super(WebServer, self).start()
        app = web.application(self.urls, globals())
        app.run()



class Values:
    def GET(self):
        return rasp_server.get_values("last")


class Value:
    def GET(self, sensor):
        return rasp_server.get_values("last")[int(sensor)]


class Min:
    def GET(self, sensor):
        return rasp_server.get_values("min")[int(sensor)]

class SetMin:
    def GET(self, sensor, value):
        rasp_server.set_min(int(sensor), int(value))
        return "Ok"


class Max:
    def GET(self, sensor):
        return rasp_server.get_values("max")[int(sensor)]

class SetMax:
    def GET(self, sensor, value):
        rasp_server.set_max(int(sensor), int(value))
        return "Ok"


class Def:
    def GET(self, sensor):
        return rasp_server.get_values("def")[int(sensor)]

class SetDef:
    def GET(self, sensor, value):
        rasp_server.set_def(int(sensor), int(value))
        return "Ok"


class Cc:
    def GET(self, sensor):
        return rasp_server.get_values("cc")[int(sensor)]

class SetCc:
    def GET(self, sensor, value):
        rasp_server.set_cc(int(sensor), int(value))
        return "Ok"


class Sens:
    def GET(self, sensor):
        return rasp_server.get_values("sens")[int(sensor)]

class SetSens:
    def GET(self, sensor, value):
        rasp_server.set_sens(int(sensor), int(value))
        return "Ok"

class Time:
    def GET(self, sensor):
        return str(int(rasp_server.get_values("time")[int(sensor)])*1000)

class SetTime:
    def GET(self, sensor, value):
        rasp_server.set_time(int(sensor), int(value))
        return "Ok"

class Save:
    def GET(self):
        rasp_server.save_config()

class Shutdown:
    def GET(self):
        rasp_server.shutdown()
        # sys.exit()
