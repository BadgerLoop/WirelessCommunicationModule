import riffle
from riffle import want
import time
import random
import os
from multiprocessing import Process

ep = os.environ.get('DATA_EP',"data")
cmd = os.environ.get('CMD_EP',"cmd")
fabric = os.environ.get('FABRIC',"ws://192.168.1.99:8000")

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
wait = 0.08


# distance travelled  0-5280
# distance to breaking   4280 decreases to - 1000

def initialize(sender):

    
    data = {"velocity":0,"state":0,"start":True,"launch":False,"stop":False,"mcm_prog":0,"bcm_prog":0,"vsm_prog":0,"vnm_prog":0,"accel_prog":0,"coast_prog":0,"node1_prog":0,"node2_prog":0,"node3_prog":0,"node4_prog":0}
    data["lw1_rpm"] = 0
    data["lw2_rpm"] = 0
    data["rw1_rpm"] = 0
    data["rw2_rpm"] = 0
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
    data["node1_prog"] = 100
    data["node2_prog"] = 100
    data["node3_prog"] = 100
    data["node4_prog"] = 100
    print("Initializing Modules... ")
    while data["mcm_prog"] < 100 or data["bcm_prog"] < 100 or data["vsm_prog"] < 100 or data["vnm_prog"] < 100:
      data["mcm_prog"] = data["mcm_prog"] + random.randint(0,4)
      data["bcm_prog"] = data["bcm_prog"] + random.randint(0,4)
      data["vsm_prog"] = data["vsm_prog"] + random.randint(0,4)
      data["vnm_prog"] = data["vnm_prog"] + random.randint(0,4)
      sender.publish(ep, data)
      time.sleep(wait)
    data["state"] = 5
    data["mcm_prog"] = 100
    data["bcm_prog"] = 100
    data["vsm_prog"] = 100
    data["vnm_prog"] = 100
    sender.publish(ep, data)
    print("Initialization Complete")

def accelerate(sender,data):
	print("Accellerating...")
	data = data
	data["state"] = 1
	while data["velocity"] < velocity_max:

		data["dt"] = ((data["accel_prog"]+data["coast_prog"]+data["slow_prog"]) * total_distance)/100
		data["db"] = dtb - ((data["accel_prog"]+data["coast_prog"]) * dtb)/50

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
		data["db"] = dtb - ((data["accel_prog"]+data["coast_prog"]) * dtb)/50

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
	data["db"] = 0
	data["state"] = 3
	while data["velocity"] > v_range_offset:
		progress = data["accel_prog"]+data["coast_prog"]+data["slow_prog"]
		data["dt"] = (progress * total_distance)/100
		data["db"] = (data["slow_prog"] * -20) - (10 + random.randint(0,9))

		data["lw1_rpm"] = (data["velocity"] * 20) + random.randint(0,w_range_offset)
		data["lw2_rpm"] = (data["velocity"] * 20) + random.randint(0,w_range_offset)
		data["rw1_rpm"] = (data["velocity"] * 20) + random.randint(0,w_range_offset)
		data["rw2_rpm"] = (data["velocity"] * 20) + random.randint(0,w_range_offset)

		data["lw1_tmp"] = temp_min + data["velocity"]/3 + random.randint(0,t_range_offset)
		data["lw2_tmp"] = temp_min + data["velocity"]/3 + random.randint(0,t_range_offset)
		data["rw1_tmp"] = temp_min + data["velocity"]/3 + random.randint(0,t_range_offset)
		data["rw2_tmp"] = temp_min + data["velocity"]/3 + random.randint(0,t_range_offset)

		data["velocity"] = data["velocity"] - 2

		if data["velocity"] > 0:
			data["slow_prog"] = 50 - (data["velocity"]/4)
		else:
			data["slow_prog"] = 50

		sender.publish(ep, data)
		time.sleep(wait)

	# Hack to make the values look right at the end
	data["db"] = -1000
	data["dt"] = total_distance

	while data["lw1_rpm"] > 0 and data["lw2_rpm"] > 0 and data["rw1_rpm"] > 0 and data["rw2_rpm"] > 0:
		data["lw1_rpm"] = data["lw1_rpm"] - 20
		data["lw2_rpm"] = data["lw2_rpm"] - 20
		data["rw1_rpm"] = data["rw1_rpm"] - 20
		data["rw2_rpm"] = data["rw2_rpm"] - 20

		if data["lw1_rpm"] <= 0 or data["lw2_rpm"] <= 0 or data["rw1_rpm"] <= 0 or data["rw2_rpm"] <= 0:
			break
		else:
			sender.publish(ep, data)
		time.sleep(wait)

	data["dt"] = 0
	data["db"] = dtb
	data["state"] = 4
	data["stop"] = True
	data["launch"] = False
	data["velocity"] = 0
	data["lw1_rpm"] = 0
	data["lw2_rpm"] = 0
	data["rw1_rpm"] = 0
	data["rw2_rpm"] = 0
	time.sleep(wait)
	sender.publish(ep, data)
		


def run(sender):
    print("Starting Simulation...")
    data = {"state":4,"lw1_rpm":0,"lw2_rpm":0,"rw1_rpm":0,"rw2_rpm":0,"lw1_tmp":0,"lw2_tmp":0,"rw1_tmp":0,"rw2_tmp":0,"velocity":0,"accel_prog":0,"coast_prog":0,"slow_prog":0,"launch":True,"start":False,"stop":False,"dt":0,"db":0}
    accelerate(sender,data)
    coast(sender,data)
    brake(sender,data)
    print("Simulation Complete")

class Send(riffle.Domain):

    def onJoin(self):
    	print("Connected to Exis Node")
        self.subscribe(cmd, self.subscription)

    @want(str)
    def subscription(self, command):
        print("Received message %s\n" %(command,))
        # if not running:
        if command == "run":
            running = True
            run(self)
            running = False
        elif command == "init":
            running = True
            initialize(self)
            running = False
    # else:
        #print("Simulation running, can't run another simulation")

if __name__ == '__main__':
    #riffle.SetLogLevelDebug()
    riffle.SetFabric(fabric)
    domain = 'xs.node'
    Send(domain).join()
    exit()