#!/usr/bin/env python

import time
import os
import sys
import subprocess
import json
import argparse


parser = argparse.ArgumentParser(description="A Script for running tests via the Badgerloop WCM")
parser.add_argument('-t','--test_file',default='ex_test.json',help="Location of test json file (must be in format outlined in ex_test.json.)",metavar="test_file")
parser.add_argument('-i','--can_interface',default="can1", help="can interface used to read message from the bus",metavar="can_interface")
parser.add_argument('-v','--validate',default=False, help="can interface used to read message from the bus",metavar="validate")
args = vars(parser.parse_args())
print(args)
with open(args['test_file']) as test_file:    
    test = json.load(test_file)

def validate_output(data):
  print(data)
	#TODO implement output validation logic


def run_test():
  for message in test['messages']:
    start_time = time.time() * 1000 #Time of sent can message in ms
    print(((time.time()*1000) - start_time))
    while ((time.time()*1000) - start_time) < message['interval_ms']:
        #Send message to CAN bus 
        subprocess.call('cansend can1 %s'%message['can'] , shell=True)
        # Get CAN message from bus
        if args['validate']:
          p = subprocess.Popen(['candump','-L','-n','1',args['can_interface']],stdout=subprocess.PIPE)
          out = p.stdout.readline()
          # Validatate output (optional)
          validate_output(out)


        print("Sent CAN message: %s \nWaiting %s ms" %(message['can'], message['interval_ms']))

if __name__ == '__main__':
   run_test()