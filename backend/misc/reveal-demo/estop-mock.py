import riffle
from riffle import want
import time
import random
import os
from multiprocessing import Process

ep = os.environ.get('DATA_EP',"estop")
cmd = os.environ.get('CMD_EP',"estopcmd")
fabric = os.environ.get('FABRIC',"ws://192.168.1.99:8000")

running = False
rpm_max = 5000
temp_max = 90
temp_min = 20
velocity_max = 200
t_range_offset = 4
w_range_offset = 100
v_range_offset = 3
coast_count = 80
total_distance = 5280

ebrake_count = 
dtb = 4280
wait = 0.08

def brake(sender,data):
	print("Emergency Stopping...")
	count = 0
	data = data
	data["db"] = 0
	while count < ebrake count:
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

		data["velocity"] = data["velocity"] - random.randint(0,v_range_offset) - 1

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
    def subscription(self, data):
        print("Received message %s\n" %(command,))
        # if not running:
        estop(self,data)
    # else:
        #print("Simulation running, can't run another simulation")

if __name__ == '__main__':
    #riffle.SetLogLevelDebug()
    riffle.SetFabric(fabric)
    domain = 'xs.node'
    Send(domain).join()
    exit()