import riffle
from riffle import want
import time
import random
import os

ep = "exis"

running = False
rpm_max = 5000
temp_max = 90
temp_min = 20
velocity_max = 200
t_range_offset = 4
w_range_offset = 100;
v_range_offset = 3;
coast_count = 80;
total_distance = 5280
dtb = 4280
wait = 0.1


# distance travelled  0-5280
# distance to breaking   4280 decreases to - 1000

def initialize(sender):

    running = True
    data = {"state":0,"start":1,"launch":0,"mcm_prog":0,"bcm_prog":0,"vsm_prog":0,"vnm_prog":0,"accel_prog":0,"coast_prog":0,"node1_prog":0,"node2_prog":0,"node3_prog":0,"node4_prog":0}
    sender.publish(ep, data)
    time.sleep(0.05)
    print("Initializing Nodes... ")
    while data["node1_prog"] < 100 or data["node2_prog"] < 100 or data["node3_prog"] < 100 or data["node4_prog"] < 100:
      data["node1_prog"] = data["node1_prog"] + random.randint(0,4)
      data["node2_prog"] = data["node2_prog"] + random.randint(0,4)
      data["node3_prog"] = data["node3_prog"] + random.randint(0,4)
      data["node4_prog"] = data["node4_prog"] + random.randint(0,4)
      sender.publish(ep, data)
      time.sleep(wait)
    print("Initializing Modules... ")
    while data["mcm_prog"] < 100 or data["bcm_prog"] < 100 or data["vsm_prog"] < 100 or data["vnm_prog"] < 100:
      data["mcm_prog"] = data["mcm_prog"] + random.randint(0,4)
      data["bcm_prog"] = data["bcm_prog"] + random.randint(0,4)
      data["vsm_prog"] = data["vsm_prog"] + random.randint(0,4)
      data["vnm_prog"] = data["vnm_prog"] + random.randint(0,4)
      sender.publish(ep, data)
      time.sleep(wait)
    running = False

def accelerate(sender,data):
	print("Accellerating...")
	data = data
	data["state"] = 1
	while data["velocity"] < velocity_max:

		data["dt"] = ((data["accel_prog"]+data["coast_prog"]+data["slow_prog"]) * total_distance)/100
		data["db"] = dtb -  data["dt"]

		data["lw1_rpm"] = (data["velocity"]  * 20) + random.randint(0,w_range_offset)
		data["lw2_rpm"] = (data["velocity"]  * 20) + random.randint(0,w_range_offset)
		data["rw1_rpm"] = (data["velocity"]  * 20) + random.randint(0,w_range_offset)
		data["rw2_rpm"] = (data["velocity"]  * 20) + random.randint(0,w_range_offset)

		data["lw1_tmp"] = temp_min + data["velocity"] /3 + random.randint(0,t_range_offset)
		data["lw2_tmp"] = temp_min + data["velocity"] /3 + random.randint(0,t_range_offset)
		data["rw1_tmp"] = temp_min + data["velocity"] /3 + random.randint(0,t_range_offset)
		data["rw2_tmp"] = temp_min + data["velocity"] /3 + random.randint(0,t_range_offset)
		data["velocity"] = data["velocity"] + random.randint(0,v_range_offset) + 2
		data["accel_prog"] = data["velocity"] /6

		sender.publish(ep, data)
		time.sleep(wait)
	data["accel_prog"] = 33

def coast(sender,data):
	print("Coasting...")
	data = data
	data["state"] = 2
	count = 0;
	while count < coast_count:

		data["dt"] = ((data["accel_prog"]+data["coast_prog"]+data["slow_prog"]) * total_distance)/100
		data["db"] = dtb - data["dt"]

		data["lw1_rpm"] = rpm_max + random.randint(0,w_range_offset)
		data["lw2_rpm"] = rpm_max + random.randint(0,w_range_offset)
		data["rw1_rpm"] = rpm_max  + random.randint(0,w_range_offset)
		data["rw2_rpm"] = rpm_max  + random.randint(0,w_range_offset)

		data["lw1_tmp"] = temp_max + random.randint(0,t_range_offset)
		data["lw2_tmp"] = temp_max + random.randint(0,t_range_offset)
		data["rw1_tmp"] = temp_max + random.randint(0,t_range_offset)
		data["rw2_tmp"] = temp_max + random.randint(0,t_range_offset)

		data["velocity"] = velocity_max + random.randint(0,v_range_offset)
		data["coast_prog"] = count/5 + 2
	
		sender.publish(ep, data)
		time.sleep(wait)
		count = count+1

def brake(sender,data):
	print("Braking/Decelerating...")
	data = data
	while data["velocity"] > v_range_offset:

		data["dt"] = ((data["accel_prog"]+data["coast_prog"]+data["slow_prog"]) * total_distance)/100
		data["db"] = dtb - data["dt"]

		data["lw1_rpm"] = (data["velocity"] * 20) + random.randint(0,w_range_offset)
		data["lw2_rpm"] = (data["velocity"] * 20) + random.randint(0,w_range_offset)
		data["rw1_rpm"] = (data["velocity"] * 20) + random.randint(0,w_range_offset)
		data["rw2_rpm"] = (data["velocity"] * 20) + random.randint(0,w_range_offset)

		data["lw1_tmp"] = temp_min + data["velocity"]/3 + random.randint(0,t_range_offset)
		data["lw2_tmp"] = temp_min + data["velocity"]/3 + random.randint(0,t_range_offset)
		data["rw1_tmp"] = temp_min + data["velocity"]/3 + random.randint(0,t_range_offset)
		data["rw2_tmp"] = temp_min + data["velocity"]/3 + random.randint(0,t_range_offset)

		data["velocity"] = data["velocity"] - random.randint(0,v_range_offset) - 2

		if data["velocity"] > 0:
			data["slow_prog"] = 50 - (data["velocity"]/4)
		else:
			data["slow_prog"] = 50

		sender.publish(ep, data)
		time.sleep(wait)

	while data["lw1_rpm"] > 40 or data["lw2_rpm"] > 40 or data["rw1_rpm"] > 40 or data["rw2_rpm"] > 40:
		data["lw1_rpm"] = data["lw1_rpm"] - 10
		data["lw2_rpm"] = data["lw2_rpm"] - 10
		data["rw1_rpm"] = data["rw1_rpm"] - 10
		data["rw2_rpm"] = data["rw2_rpm"] - 10
		sender.publish(ep, data)
		time.sleep(wait)

	data["dt"] = 0
	data["db"] = dtb
	data["state"] = 4
	data["launch"] = 0
	data["velocity"] = 0
	data["lw1_rpm"] = 0
	data["lw2_rpm"] = 0
	data["rw1_rpm"] = 0
	data["rw2_rpm"] = 0

	print(data)
	time.sleep(wait)
	sender.publish(ep, data)
		


def run(sender):
    running = True
    print("Starting Simulation...")
    data = {"state":4,"lw1_rpm":0,"lw2_rpm":0,"rw1_rpm":0,"rw2_rpm":0,"lw1_tmp":0,"lw2_tmp":0,"rw1_tmp":0,"rw2_tmp":0,"velocity":0,"accel_prog":0,"coast_prog":0,"slow_prog":0,"launch":1,"start":0,"dt":0,"db":0}
    accelerate(sender,data)
    coast(sender,data)
    brake(sender,data)
    running = False

class Send(riffle.Domain):

    def onJoin(self):
        self.subscribe("cmd", self.subscription)
        self.subscribe("stop", self.stop)

    @want(str)
    def subscription(self, command):
        print("Received message %s\n" %(command,))
        if not running:
            if command == "run":
                run(self)
            elif command == "init":
                initialize(self)
        else:
        	print("Simulation running, can't run another simulation")
    @want(str)  	
    def stop(self, command):
     	print("Received message %s\n" %(command,))

if __name__ == '__main__':
    #riffle.SetLogLevelDebug()
    riffle.SetFabric('ws://192.168.1.99:8000')
    domain = 'xs.node'
    Send(domain).join()
    exit()