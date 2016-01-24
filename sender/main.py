import os
#import exis
from multiprocessing import Process


#Set up global config variables here




def _case_1(data):
	print('Case 1 for message type: ...')
	#Convert data for module (TBD)
	rpm_data = (float(data[2]))
	send(rpm_data)

def _case_2(data):
	print('Case 2 for message type: ...')
	#Convert data for module (TBD)
	deg_C_data = (float(data[2]))
	send(deg_C_data)

 def _case_3(data):
	print('Case 3 for message type: ...')
	#Convert data for module (TBD)
	deg_C_data = (float(data[2]))
	send(deg_C_data)

#TODO: FIND OUT WHAT VALUES TO SEND
 def _case_4(data):
	print('Case 4 for message type: ...')
	#Convert data for module (TBD)
	formatted_data = None
	send(formatted_data)

#TODO: FIND OUT WHAT VALUES TO SEND
def _case_5(data):
	print('Case 5 for message type: ...')
	#Convert data for module (TBD)
	formatted_data = None
	send(formatted_data)

 def _case_6(data):
	print('Case 6 for message type: ...')
	#Convert data for module (TBD)
	millimeters_data = (float(data[2]))
	send(millimeters_data)

 def _case_7(data):
	print('Case 7 for message type: ...')
	#Convert data for module (TBD)
	milliseconds_data = (float(data[2]))
	send(milliseconds_data)

 def _case_8(data):
	print('Case 8 for message type: ...')
	#Convert data for module (TBD)
	volts_data = (float(data[2]))
	send(volts_data)



def send(formatted_data):
	print('Sent CAN message to exis endpoint')



def main():

#Read can message input from source (TBD)
    data = subprocess.check_output("./can_parse_single", shell=True).decode('utf-8').rstrip('\n').split('_')
    key = data[1]

# Define switch statement
    switch = { 'optEn':_case_1(data),
               'therm1':_case_2(data),
               'therm2':_case_3(data),
               'accel':_case_4(data),
               'gyro':_case_5(data),
               'prox':_case_6(data),
               'latency':_case_7(data),
               'battVolt':_case_8(data)
    }

#Run message decoding and sending in separate processes to improve throughput
    p = Process(target=switch[key], args=(data,))
    p.start()
    p.join()


if __name__ == "__main__":
	main()
