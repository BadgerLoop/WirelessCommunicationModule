import riffle
import time
import os
import sys
import random
import argparse
import json
import math
import struct
import binascii

parser = argparse.ArgumentParser(description="A script for spamming the Exis node backend with random data")
parser.add_argument('-p','--parser',default='../app/parser.json',help="Location of parser json file",metavar="parser")
parser.add_argument('-f','--frequency_hz',default=1, help="Frequency in hertz of messages sent over the network. Defaults to 10",metavar="frequency_hz")
parser.add_argument('-b','--batch_size',default=5, help="Size of CAN message batches. Defaults to 5",metavar="batch_size")
parser.add_argument('-i','--can_interface',default="can1", help="can interface used to read message from the bus",metavar="can_interface")
parser.add_argument('-l','--backend_location',default="ws://localhost:8000", help="Location of backend.  Defaults to ws://localhost:8000",metavar="backend")
parser.add_argument('-sb','--spam_bus',default=False, help="Boolean: spam CAN bus on the WCM. Defaults to True",metavar="spam_bus")
args = vars(parser.parse_args())

with open(args['parser']) as parser_file:    
    parser = json.load(parser_file)

def pick_message():
    rand_msg = random.choice(parser['messages'])
    #print(rand_msg)
    return rand_msg

def generate_sid(module):
    if module is not 'ALL' and 'from' in parser['SID'][module]:
        int_sid = parser['SID'][module]['from']
        sid = "{0:0{1}X}".format(int_sid,3)
        #print(sid)
    else:
        sid = '000'
    return sid

def encode_data(data, bytes):
    encoding = [
                {'mask':0xFF, 'format_str': "%01X"},
                {'mask':0xFFFF, 'format_str': "%02X"},
                {'mask':0xFFFFFF, 'format_str':"%03X"},
                {'mask':0xFFFFFFFF, 'format_str': "%04X"},
                {'mask':0xFFFFFFFFFF, 'format_str': "%05X"},
                {'mask':0xFFFFFFFFFFFF, 'format_str': "%06X"},
                {'mask':0xFFFFFFFFFFFFFF, 'format_str': "%07X"}
                ]
    print(data)
    encoded_data = encoding[bytes]['format_str'] % (data & encoding[bytes]['mask'],)
    #print(encoded_data)
    return encoded_data 



def generate_message():
    print("Generating random message")
    data_hex = ""
    msg_spec = pick_message()
    #print(msg_spec)
    while msg_spec['cmd']:
        msg_spec = pick_message()

    msg_type = '{:02x}'.format(msg_spec['id'])
    module = msg_spec['module']
    sid = generate_sid(module)

    for val in msg_spec['values']:
        #print(val.keys()[0])
        if 'state' not in val or 'bool' not in val:
            off = val['nominal_high'] * .1
            high = val['nominal_high'] + off
            low = val['nominal_low'] - off
            byte_size = val['byte_size']
            scalar = val['scalar']
            data = int(random.uniform(low,high)/scalar)
            #fstring = '{:0' + str(byte_size*2) + 'x}'
            #print("0x%08X\n", x)f string.format(data)
            data_hex = data_hex + encode_data(data, byte_size)
            #print(data_hex)
            #print("Size: %s" %byte_size)

        elif 'bool' in val:
            data = int(random.randint(0, 1))
        else:
            data = int(random.randint(0, 1))

    
    print("SID: %s Type: %s Data: %s " %(sid,msg_type,data_hex))
    return sid, msg_type, data_hex




class spammer(riffle.Domain):
    def send_exis(self,batch):
        self.publish("can", batch)

    def send_can(self,sid,msg_type,data):
        self.publish("cmd", "%s#%s%s" %(sid,msg_type,data))

    def onJoin(self):
        print("Connected to Exis Node at %s" % args['backend_location'])
        sleep_time = math.pow(int(args['frequency_hz']), -1)
        while True:
            if bool(args['spam_bus']):
                sid, msg_type, data = generate_message()
                self.send_can(sid, msg_type, data)
                #subprocess.call('cansend %s %s#%s%s'%(args['can_interface'],sid,msg_type,data) , shell=True)
            else:
                batch = []
                for i in range(0,int(args['batch_size'])):
                    sid, msg_type, data = generate_message()
                    batch.append([time.time(),sid,msg_type,data])
                self.send_exis(batch)
            #self.publish("can",[[str(current_milli_time()),"100","00","00 00"],[str(current_milli_time()),"100","00","00 00"]]) # Using for tests
            wait_time = (1/int(args['frequency_hz']))
            time.sleep(sleep_time)

if __name__ == '__main__':
    print("Starting exis node spammer")
    print(args['backend_location'])
    riffle.SetFabric(args['backend_location'])
    spammer('xs.node').join()