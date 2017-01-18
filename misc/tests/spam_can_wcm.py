import time
import os
import sys
import subprocess

interval_ms = int(sys.argv[1])

def spam():
    while True:
        sid = "0" + str(os.urandom(1).encode('hex')) 
        data = str(os.urandom(2).encode('hex'))
        raw  = sid + "#" + data 
        subprocess.call('cansend can1 '+ raw, shell=True)
        print("Sent WCM can message: " + raw)
        time.sleep(float(interval_ms*.001))

if __name__ == '__main__':
    spam()