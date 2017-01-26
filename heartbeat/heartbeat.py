import riffle
from riffle import want
import time
import os
import subprocess
import argparse
import json
import re

parser = argparse.ArgumentParser(description="A script for converting raw can messages to correct values")
parser.add_argument('-p','--parser',default='../dashboard/app/parser.json',help="Location of parser json file",metavar="parser")
parser.add_argument('-l','--backend_location',default="ws://localhost:8000", help="Location of backend.  Defaults to ws://localhost:8000",metavar="backend")
args = vars(parser.parse_args())

with open(args['parser']) as parser_file:    
    parser = json.load(parser_file)

current_milli_time = lambda: int(round(time.time() * 1000))

class Heartbeat():
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.fault_count = 0
        self.fault_max = 0
        self.interval_ms = 1000
        self.rx_hb_empty = True
        self.timer = time.time()
        self.modules = {
                'VSM' :{'prev_fault':0, 'fault': 0,'prev': 1, 'cur':1, 'next': 1, 'last_updated':time.time()},
                'BCM' :{'prev_fault':0, 'fault': 0,'prev': 1, 'cur':1, 'next': 1, 'last_updated':time.time()},
                'MCM' :{'prev_fault':0, 'fault': 0,'prev': 1, 'cur':1, 'next': 1, 'last_updated':time.time()},
                'WCM' :{'prev_fault':0, 'fault': 0,'prev': 1, 'cur':1, 'next': 1, 'last_updated':time.time()},
                'VNM' :{'prev_fault':0, 'fault': 0,'prev': 1, 'cur':1, 'next': 1, 'last_updated':time.time()},
                'BMS' :{'prev_fault':0, 'fault': 0,'prev': 1, 'cur':1, 'next': 1, 'last_updated':time.time()}
        }

    def check_timing_fault(self):
        now = time.time()
        for k in self.modules:
            time_delta = now - self.modules[k]['last_updated']
            if time_delta > self.interval_ms:
                self.fault_count = self.fault_count + 1
        self.fault_count = 0


    def generate_status(self):
        print("generating status")
        if self.fault_count>self.fault_max:
            return "FAILURE"
        for k in self.modules.keys():
            if self.modules[k]['fault'] is not 0 or self.modules[k]['fault'] in [1,6]:
                return "FAILURE"
        return "GOOD"


          
    def update_module_hb(self,module,data):
        self.modules[module]['last_updated'] = time.time()
        self.modules[module]['prev_fault']= int(data[0],16)
        self.modules[module]['fault']= int(data[1],16)
        self.modules[module]['prev']= int(data[2],16)
        self.modules[module]['cur']= int(data[3],16)
        self.modules[module]['next']= int(data[4],16)

class HB(riffle.Domain):

    def onJoin(self):
        print("Connected to Exis Node")
        self.Heartbeat = Heartbeat()
        self.subscribe("hb_ctrl", self.hb_ctrl)
        # self.subscribe("hb", self.hb_handler)
        self.subscribe("can", self.can_parser)
        self.p=None

    def send_hb(self,sid,data):
        print("updating heartbeat sid: " + str(sid))

        split_data = re.findall('..',data[3])
        # print(split_data)
        send = {}
        for module in parser['SID']:

            if 'from' in parser['SID'][module]:
                from_mask = parser['SID'][module]['from']
                # TODO Fix this logic
                and_res = int(sid,16) & from_mask
                # print(and_res)
                if and_res == from_mask and and_res != 0:
                    print("Got status for " + module)
                    self.Heartbeat.update_module_hb(module,split_data)
                    self.Heartbeat.check_timing_fault()
                    
                    send['modules'] = self.Heartbeat.modules
                    send['fault_count'] = self.Heartbeat.fault_count
                    send['system_status'] = self.Heartbeat.generate_status()
                    #print(send)
        if 'system_status' in send and (time.time() - self.Heartbeat.timer) >= self.Heartbeat.interval_ms:
            print('sending heartbeat')
            self.publish("hb",send)

    def can_parser(self,data):
        #TODO: Ensure this logic is correct
        converted_batch = []
        #print(data)
        # msg in format [timestamp,sid,msg_type,data]
        for msg in data:
            
            ts = float(msg[0])
            sid = msg[1]
            msg_type = int(msg[2],16)
            data_str = msg[3]
            if msg_type == 1:
                self.send_hb(sid,msg)
            else:
                converted_data = [ts,sid,msg_type]
                message_spec = parser['messages'][msg_type]
                for val in message_spec['values']:
                    data_value = data_str[:(val['byte_size']*2)]
                    data_str.replace(data_value,'',1)
                    # print(data_value)
                    if val['units'] in ['int','count','status','state']:
                        formatted_val = int(data_value,16)
                    else:
                        formatted_val = round(int(data_value,16)*val['scalar'],val['precision'])
                    # print(formatted_val)
                    #converted_data.append(formatted_val)
                    # if 'STRIP' in val['title']:
                    #     print(val['title'] + ": " + str(int(data_value,16)))
                    converted_batch.append([val['title'],formatted_val])
                # print("converting data")
                #converted_batch.append(converted_data)
        #print(converted_batch)
        print('Sending formatted data')
        self.publish("data",converted_batch)

    def hb_ctrl(self, data):
        if data[0] == 1:
            self.Heartbeat.fault_max = data[2]
            self.Heartbeat.interval_ms = data[1]
            self.Heartbeat.run_hb = True
            #Add more logic to check if hb is still running
            print("starting hb subprocess")
            self.p = subprocess.Popen("python hb-driver.py %s %s" %(data[1],args['backend_location']), stdout=subprocess.PIPE, shell=True)
        elif data[0] == 0:
            if self.p:
                self.p.kill()

    # def hb_handler(self, data):
    #     print("Received hb CAN message %s" %data)
    #     if self.Heartbeat.rx_hb_empty:
    #         self.Heartbeat.rx_hb[data[3]]



if __name__ == '__main__':
    #riffle.SetLogLevelDebug()
    riffle.SetFabric(args['backend_location'])
    HB('xs.node').join()

