import os

import riffle

from multiprocessing import Process


#Set up global config variables here


def _case_1(data_array):
	print('Case 1 for message type: ...')
	#Convert data for module (TBD)
	rpm_data = (float(data_array[2]))
	send(data_array,rpm_data)

def _case_2(data_array):
	print('Case 2 for message type: ...')
	#Convert data for module (TBD)
	deg_C_data = (float(data_array[2]))
	send(data_array,deg_C_data)

 def _case_3(data_array):
	print('Case 3 for message type: ...')
	#Convert data for module (TBD)
	deg_C_data = (float(data_array[2]))
	send(data_array,deg_C_data)

 def _case_4(data_array):
	print('Case 4 for message type: ...')
	#Convert data for module (TBD)
	vcm_accel_data = float(data_array[2]).extend(float(data_array[3])).extend(float(data_array[4]))
	send(data_array,vcm_accel_data)

def _case_5(data_array):
	print('Case 5 for message type: ...')
	#Convert data for module (TBD)
	vcm_gyro_data = float(data_array[2]).extend(float(data_array[3])).extend(float(data_array[4]))
	send(data_array,vcm_gyro_data)

 def _case_6(data_array):
	print('Case 6 for message type: ...')
	#Convert data for module (TBD)
	millimeters_data = (float(data_array[2]))
	send(data_array,millimeters_data)

 def _case_7(data_array):
	print('Case 7 for message type: ...')
	#Convert data for module (TBD)
	milliseconds_data = (float(data_array[2]))
	send(data_array,milliseconds_data)

 def _case_8(data_array):
	print('Case 8 for message type: ...')
	#Convert data for module (TBD)
	volts_data = (float(data_array[2]))
	send(data_array,volts_data)


# Send formatted data to Exis endpoints
def send(data_array,formatted_data):
    endpoint = data_array[0] + "_" + data_array[1]
    backend.publish(endpoint, formatted_data)
	print('Sent CAN message ' + formatted_data + ' to exis endpoint')



def main():

    
    class Backend(riffle.Domain):

        def onJoin(self):
        	print("Successfully joined")

    
    app = riffle.Domain("xs.demo.badgerloop.bldashboard")
    backend = riffle.Domain("backend", superdomain=app)
    DataProvider("datasource", superdomain=app).join()

    # Define switch statement
    while 1:
        data = subprocess.check_output("./can_parse_single", shell=True).decode('utf-8').rstrip('\n').split('_')
        switch = { 'bpm':_bpm, #keys for cases should be the prifix of the raw data string?
                   'ecm':_ecm,
                   'vcm':_vcm,
                   'mcm':_mcm,
                   'wcm':_wcm,
                   'bpm2':_bpm2
                 }

        # Run message decoding and sending in separate processes to improve throughput 
        p = Process(target=switch[data[0]], args=(data,backend))
        p.start()
        p.join()

if __name__ == "__main__":
	main()
