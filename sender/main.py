import os
import riffle
import subprocess
import yaml
from multiprocessing import Process

def _bpm(data_array, backend):
    print('Parcing bpm data')
    rpm_data = (float(data_array[2]))
    send(data_array,rpm_data, backend)

def _bpm2(data_array, backend):
    print('Parsing bpm2 data')
    volts_data = (float(data_array[2]))
    send(data_array,volts_data, backend)

def _ecm(data_array, backend):
    print('Parcing ecm data')
    deg_C_data = (float(data_array[2]))
    send(data_array,deg_C_data, backend)

def _vcm(data_array, backend):
    print('Parcing vcm data')
    if data_array[1] is 'gyro':
        vcm_gyro_data = float(data_array[2]).extend(float(data_array[3])).extend(float(data_array[4]))
        send(data_array,vcm_gyro_data, backend)
    elif data_array[1] is 'accel':
        vcm_accel_data = float(data_array[2]).extend(float(data_array[3])).extend(float(data_array[4]))
        send(data_array,vcm_accel_data, backend)

def _mcm(data_array, backend):
    print('Parcing mcm data')
    millimeters_data = (float(data_array[2]))
    send(data_array,millimeters_data, backend)
    
def _wcm(data_array, backend):
    print('Parcing wcm data')
    milliseconds_data = (float(data_array[2]))
    send(data_array,milliseconds_data, backend)
    
def send(data_array,formatted_data, backend):
    # Send formatted data to Exis endpoints
    endpoint = data_array[0] + "_" + data_array[1]
    backend.publish(endpoint, formatted_data)
    print('Sent CAN data: ' + formatted_data + ' to exis endpoint: ' + endpoint)


class DataProvider(riffle.Domain):

    def onJoin(self):
        print("Successfully joined")

    
def main():

    with open('config.yml') as config_data:
        config = yaml.safe_load(config_data)
    app = riffle.Domain(config['exis']['domain'])
    riffle.SetFabric(config['exis']['localFabric']) #For local fabric - will need to change to static IP
    backend = riffle.Domain("backend", superdomain=app)
    datasource = DataProvider("datasource", superdomain=app).join()
    switch = { 'bpm':_bpm, #keys for cases should be the prifix of the raw data string?
               'ecm':_ecm,
               'vcm':_vcm,
               'mcm':_mcm,
               'wcm':_wcm,
               'bpm2':_bpm2
            }

    while True:
        try:
            data = subprocess.check_output(config['buffer'], shell=True).decode('utf-8').rstrip('\n').split('_')
        except Exception as e:
            print('Unable to retrieve CAN message.  Exception: %s' % (str(e),))

        if data is not None and data[0] in switch:
            p = Process(target=switch[data[0]], args=(data, backend))
            p.start()
            p.join()

if __name__ == "__main__":
    main()
