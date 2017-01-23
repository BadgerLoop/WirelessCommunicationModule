import time
import os
import sys
import subprocess
import json
import argparse


parser = argparse.ArgumentParser(description="A CLI for implementing String Functions over SPU ")
parser.add_argument('-t','--test_file',default='ex_test.json',help="Location of test json file (must be in format outlined in ex_test.json.)",metavar="test_file")
parser.add_argument('-i','--can_interface',default="can1", help="can interface used to read message from the bus",metavar="can_interface")
args = vars(parser.parse_args())
print(args)
with open(args['test_file']) as test_file:    
    test = json.load(test_file)

def validate_output(data):
	#TODO implement output validation logic
	pass

def run_test():
  for message in test['messages']:
    start_time = time.time() * 1000 #Time of sent can message in ms
    while ((time.time()*1000) - start_time) < message['interval_ms']:
      	subprocess.Popen(['candump','-L','-n','1','can1'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        validate_output(out)

        subprocess.call('cansend can1 %s'%message['can'] , shell=True)
        print("Sent CAN message: %s \nWaiting %s ms" %(message['can'], message['interval_ms']))

if __name__ == '__main__':
   run_test()