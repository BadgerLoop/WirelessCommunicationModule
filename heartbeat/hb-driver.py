import riffle
import time
import os
import sys

fabric = "ws://192.168.1.99:9000"
interval_ms = int(sys.argv[1])
class HB(riffle.Domain):

    def onJoin(self):
        print("Connected to Exis Node")
        while True:
            self.publish("can","5C0#1301")
            self.publish("hb","5C0#1301")
            print("Sent WCM heartbeat")
            time.sleep(interval_ms/1000)
            print("waiting...")

if __name__ == '__main__':
    print("Starting HB Driver")
    riffle.SetFabric(fabric)
    HB('xs.node').join()