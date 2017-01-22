#!/usr/bin/env python
"""
@brief Hyperloop team telemetry packet sender 
@author Kyle Grieger

Subject to the existing rights of third parties, SPACE EXPLORATION
TECHNOLOGIES is the owner of the copyright in this work and no portion
thereof is to be copied, reproduced or communicated to any person without
written permission.
"""
import socket
import struct
import time
import riffle
from datetime import datetime
#import ctypes 
#c_int8

team_id = bytes(1) #change this to what team id spacex gives us

class telemetry():
    def __init__(self):
        self.wcm_status = 0
        self.mcm_status = 0
        self.vnm_status = 0
        self.vsm_status = 0
        self.bcm_status = 0
        self.status = 0
        self.position = 0
        self.position_scalar = 2.594 # centimeter
        self.velocity = 0
        self.velocity_scalar = 0.168 # centimeter/s
        self.acceleration = 0
        self.acceleration_scalar = 0.122 # centimeter/s^2
        self.voltage = 0
        self.voltage_scalar = 2.32 # in mvolts
        self.current = None
        self.current_scalar = 15.26
        self.bat_temp = None
        self.bat_temp_scalar = 58594
        self.pod_temp = None
        self.pod_temp_scalar = 58594
        self.stripe_count = 0
        self.frequency_hz = 10 
        self.interval_ms = 1/self.frequency_hz # Make configurable with environment variable
        self.ts = datetime.now()

    def update_status(self,sid,data):
        #TODO: implement status logic to form overall status analysis
        status = int(data[:2],16)
        
    def update_pos(self,sid,data):
        self.position = bytes(int(data[:4],16) * self.position_scalar)
        print('updated position. Value: %s'  %self.position)

    def update_vel(self,sid,data):
        self.velocity = bytes(int(data[:4],16) * self.velocity_scalar)
        print('updated velocity. Value: %s'  %self.velocity)

    def update_accel(self,sid,data):
        self.acceleration = bytes(int(data[:4],16) * self.acceleration_scalar)
        print('updated acceleration. Value: %s'  %self.acceleration)

    def update_bat_temp(self,sid,data):
        self.bat_temp = bytes(int(data[:4],16) * self.bat_temp_scalar)
        print('updated bat_temp. Value: %s'  %self.bat_temp) 
        pass

    def update_pod_temp(self,sid,data):
        self.pod_temp = bytes(int(data[:2],16) * self.pod_temp_scalar)
        print('updated pod_temp. Value: %s'  %self.pod_temp) 

    def update_bat_current(self,sid,data):
        # TODO implement this using BMS messages tbd
        # self.current = bin(int(data[:4],16) * self.current_scalar )
        # print('updated bat_current. Value: %s'  %self.current) 
        pass
    def update_bat_voltage(self,sid,data):
        # TODO implement this using BMS messages tbd
        # self.voltage= bin(int(data[:4],16) * self.voltage_scalar )
        # print('updated bat_voltage. Value: %s'  %self.voltage) 
        pass

    def check_if_valid(self):
        #TODO: check if current values in object are valid
        pass

    def update_stripe_count(self,sid,data):
        self.stripe_count = bin(int(data[:4],16) * self.stripe_count)
        print('updated stripe_count. Value: %s'  %self.voltage) 

    def update_telemetry(self,sid,msg_id,data):
        update_telemetry =  {
                '01': self.update_status,
                '04': self.update_pos,
                '05': self.update_vel,
                '06': self.update_pos,
                '09': self.update_bat_temp,  # Double check that this is the correct 
                '0A': self.update_pod_temp,
                'XX': self.update_bat_current, # Update this, will come from the BMS
                'XX': self.update_bat_voltage, # Update this, will come from the BMS
                'XX': self.update_stripe_count # Update this.  New message to be created
        }
        update_telemetry[msg_id](sid,data)

    def send_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.bind(('localhost', 3000)) 
        UDP_IP = 'localhost'
        UDP_PORT = 3000
        pattern = '!BBi7I'
        packet = struct.pack(pattern, 
            team_id,
            self.status,
            self.accel,
            self.position,
            self.velocity,
            self.voltage,
            self.current,
            self.bat_temp,
            self.pod_temp,
            self.stripe_count) # Make sure that these values fit into the struct appropriately
        sock.sendto(packet, (UDP_IP, UDP_PORT)) # Add environment varible to define the ip of the spacex packet server

class listener(riffle.Domain):

    def onJoin(self):
        print("Connected to Exis Node")
        self.telemetry = telemetry()
        self.subscribe("can", self.can_rx)

    def can_rx(self, data):
        # Data is in format [[timestamp,sid,msg_type,data]]
        # Update telemetry data
        for d in data:
            telemetry.update_telemetry(d[1],d[2],d[3])
            
        timedelta_ms = (datetime.now() - self.telemetry.ts).microseconds/1000
        if  timedelta_ms <= interval_ms: #Verify that this works for determining when to send packet
            if self.telemetry.check_if_valid():
                self.telemetry.send_packet()
                self.telemetry.ts = datetime.now()
            # Do something if data is not valid i.e. there are null values and such
def main():
    riffle.SetFabric(fabric)
    listener('xs.node').join()
    # tel = telemetry()
    # tel.update_telemetry('blah','04','aaaa')
    # dt = datetime.now()
    # time.sleep(.01)
    # timed = datetime.now() - dt
    # print(timed.microseconds/1000)

if __name__ == "__main__":
    main()
