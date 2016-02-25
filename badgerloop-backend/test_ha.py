import os
import riffle
import random
import time

print('starting ha test')
#riffle.SetFabricLocal()
app = riffle.Domain("xs.node")
riffle.SetFabric("ws://192.168.99.100:8000/ws")
backend = riffle.Domain("backend", superdomain=app)
class DataProvider(riffle.Domain):

    def onJoin(self):
        print("Successfully joined")

        while True:
            #data = subprocess.check_output("nc -l 2999", shell=True).decode('utf-8').rstrip('\n').split('_')
            rand = random.randint(10000,80000)
            backend.publish('test',100)
            print('Sent data: ' + str(rand) + ' to exis endpoint: test')
            time.sleep(1)
   

def main():
 #For local fabric - will need to change to static IP
    try:
        datasource = DataProvider("datasource", superdomain=app).join()
    except:
        print('exception thrown')

if __name__ == "__main__":
    main()
