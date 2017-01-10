import os
import riffle
import subprocess
import yaml
from multiprocessing import Process

def _bpm(data_array):
    print('Parcing bpm data')
    rpm_data = (float(data_array[2]))
    send(data_array,rpm_data)

def _bpm2(data_array):
    print('Parsing bpm2 data')
    volts_data = (float(data_array[2]))
    send(data_array,volts_data)

def _ecm(data_array):
    print('Parcing ecm data')
    deg_C_data = (float(data_array[2]))
    send(data_array,deg_C_data)

def _vcm(data_array):
    print('Parcing vcm data')
    if data_array[1] is 'gyro':
        vcm_gyro_data = float(data_array[2]).extend(float(data_array[3])).extend(float(data_array[4]))
        send(data_array,vcm_gyro_data)
    elif data_array[1] is 'accel':
        vcm_accel_data = float(data_array[2]).extend(float(data_array[3])).extend(float(data_array[4]))
        send(data_array,vcm_accel_data)

def _mcm(data_array):
    print('Parcing mcm data')
    millimeters_data = (float(data_array[2]))
    send(data_array,millimeters_data)
    
def _wcm(data_array):
    print('Parcing wcm data')
    milliseconds_data = (float(data_array[2]))
    send(data_array,milliseconds_data)
    
def send(data_array,formatted_data):
    # Send formatted data to Exis endpoints
    endpoint = data_array[0] + "_" + data_array[1]
    backend.publish(endpoint, formatted_data)
    print('Sent CAN data: ' + formatted_data + ' to exis endpoint: ' + endpoint)


class DataProvider(riffle.Domain):

    def onJoin(self):
        print("Successfully joined")

        while True:
            #data = subprocess.check_output("nc -l 2999", shell=True).decode('utf-8').rstrip('\n').split('_')
            # switch = { 'bpm':_bpm, #keys for cases should be the prifix of the raw data string?
            #        'ecm':_ecm,
            #        'vcm':_vcm,
            #        'mcm':_mcm,
            #        'wcm':_wcm,
            #        'bpm2':_bpm2
            #      }

            # switch[data[0]](data, backend)
            switch[data[0]]('data', backend)
    
def main():
    app = riffle.Domain("xs.demo.badgerloop.bldashboard")
    riffle.SetFabric("ws://localhost:8000/ws") #For local fabric - will need to change to static IP
    backend = riffle.Domain("backend", superdomain=app)
    datasource = DataProvider("datasource", superdomain=app).join()


if __name__ == "__main__":
    main()
