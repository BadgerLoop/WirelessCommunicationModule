import riffle
from riffle import want
import time
import os
import subprocess


fabric = "ws://192.168.1.99:9000"
current_milli_time = lambda: int(round(time.time() * 1000))

class Heartbeat():
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.fault_count = 0
        self.fault_max = 0
        self.interval_ms = 1000
        self.run_hb = False
        self.rx_hb = {
                "01": None,
                "02": None,
                "03": None,
                "04": None,
                "19": None,
            }
    def validate(self):
        pass

class HB(riffle.Domain):

    def onJoin(self):
        print("Connected to Exis Node")
        self.Heartbeat = Heartbeat()
        self.subscribe("hb_ctrl", self.hb_ctrl)
        self.subscribe("hb", self.hb_handler)
        self.p=None

    def hb_ctrl(self, data):
        if data[0] == 1:
            self.Heartbeat.fault_max = data[2]
            self.Heartbeat.interval_ms = data[1]
            self.Heartbeat.run_hb = True
            #Add more logic to check if hb is still running
            print("starting hb subprocess")
            self.p = subprocess.Popen("python hb-driver.py %s" %data[1], stdout=subprocess.PIPE, shell=True)
        elif data[0] == 0:
            self.Heartbeat.run_hb = False
            self.p.kill()

    def hb_handler(self, data):
        print("Received hb CAN message %s" %data)

if __name__ == '__main__':
    #riffle.SetLogLevelDebug()
    riffle.SetFabric(fabric)
    HB('xs.node').join()

