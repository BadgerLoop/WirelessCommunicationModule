import os
#import exis
from multiprocessing import Process


#Set up global config variables here


def _case_1(data):
	print('Case 1 for message type: ...')
	#Convert data for module (TBD)
	formatted_data = None
	send(formatted_data)


def _case_2(data):
	print('Case 2 for message type: ...')
	#Convert data for module (TBD)
	formatted_data = None
	send(formatted_data)


def send(formatted_data):
	print('Sent CAN message to exis endpoint')



def main():
# Define switch statement
    switch = { '1':_case_1,
               '2':_case_2
    }

#Read can message input from source (TBD)
    key = '1'
    data = None

#Run message decoding and sending in separate processes to improve throughput 
    p = Process(target=switch[key], args=(data,))
    p.start()
    p.join()


if __name__ == "__main__":
	main()