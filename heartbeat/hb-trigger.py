import riffle
from riffle import want
import time
import os

fabric = "ws://192.168.1.99:9000"
class Backend(riffle.Domain):

    def onJoin(self):
        print("Connected to Exis Node")
        self.publish("cmd", [1,100,1000])
        self.publish("cmd", [1,100,1000])
        return

if __name__ == '__main__':
    riffle.SetLogLevelDebug()
    riffle.SetFabric("ws://192.168.1.99:9000")
    domain = 'xs.node'
    Backend(domain).join()
    exit()