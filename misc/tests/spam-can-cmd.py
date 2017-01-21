import riffle
import time
import os
import sys
import random

fabric = "ws://192.168.1.99:9000"
interval_ms = int(sys.argv[1])
current_milli_time = lambda: int(round(time.time() * 1000))
class HB(riffle.Domain):

    def onJoin(self):
        print("Connected to Exis Node")
        while True:
            # sid = "0" + str(os.urandom(1).encode('hex')) 
            # data = str(os.urandom(2).encode('hex'))
            # raw  = sid + "#" + data 
            raw = 440
            self.publish("cmd",raw)
            #self.publish("can",[[str(current_milli_time()),"100","00","00 00"],[str(current_milli_time()),"100","00","00 00"]]) # Using for tests
            print("Sent WCM cmd: " + raw)
            time.sleep(float(interval_ms*.001))

if __name__ == '__main__':
    print("Starting HB Driver")
    riffle.SetFabric(fabric)
    HB('xs.node').join()