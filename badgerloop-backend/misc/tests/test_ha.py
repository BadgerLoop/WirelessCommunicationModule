import riffle
import time
import random
import os

# riffle.SetLogLevelDebug()

modules = ["BPM1", "BPM2", "MCM", "VCM", "ECM"]
sensors = ['Shaft Encoder 1', 'Accelerometer/Gyro 1', 'Limit Switch 1', 'Limit Switch 2', 'Limit Switch 3', 'Limit Switch 4', 'Limit Switch 5', 'Limit Switch 6', 'Limit Switch 7', 'Limit Switch 8', 'Solid State Relay 1', 'Solid State Relay 2', 'Solid State Relay 3', 'Solid State Relay 4', 'Solid State Relay 5', 'Solid State Relay 6', 'Linear Actuator 1', 'Bogie Electromagnet 1', 'Bogie Electromagnet 2', 'Drum Brake Electromagnet 1', 'Drum Brake Electromagnet 2', 'Drum Brake Electromagnet 3', 'Drum Brake Electromagnet 4', 'Small Motor Controller 1', 'Shaft Encoder 1', 'Accelerometer/Gyro 1', 'Limit Switch 1', 'Limit Switch 2', 'Limit Switch 3', 'Limit Switch 4', 'Limit Switch 5', 'Limit Switch 6', 'Limit Switch 7', 'Limit Switch 8', 'Solid State Relay 1', 'Solid State Relay 2', 'Solid State Relay 3', 'Solid State Relay 4', 'Solid State Relay 5', 'Solid State Relay 6', 'Linear Actuator 1', 'Bogie Electromagnet 1', 'Bogie Electromagnet 2', 'Drum Brake Electromagnet 1', 'Drum Brake Electromagnet 2', 'Drum Brake Electromagnet 3', 'Drum Brake Electromagnet 4', 'Small Motor Controller 1', 'Pressure Transducer 1', 'Proximity Sensor 1', 'Proximity Sensor 2', 'Proximity Sensor 3', 'Proximity Sensor 4', 'Proximity Sensor 5', 'Proximity Sensor 6', 'Proximity Sensor 7', 'Proximity Sensor 8', 'Proximity Sensor 9', 'Proximity Sensor 10', 'Eddy Brake Current Sensor 1', 'Eddy Brake Current Sensor 2', 'Eddy Brake Current Sensor 3', 'Eddy Brake Current Sensor 4', 'Eddy Brake Current Sensor 5', 'Encoder 1', 'Encoder 2', 'Encoder 3', 'Encoder 4', 'Encoder 5', 'Encoder 6', 'Encoder 7', 'Encoder 8', 'Encoder 9', 'Encoder 10', 'Motor Controller 1', 'Motor Controller 2', 'Motor Controller 3', 'Motor Controller 4', 'Motor Controller 5', 'Motor Controller 6', 'Motor Controller 7', 'Motor Controller 8', 'Motor Controller 9', 'Motor Controller 10', 'Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6', 'Motor 7', 'Motor 8', 'Motor 9', 'Motor 10', 'Accelerometer/Gyro 1', 'Accelerometer/Gyro 2', 'Accelerometer/Gyro 3', 'Limit Switch 1', 'Limit Switch 2', 'Tape Strip Detector 1', 'Tape Strip Detector 2', 'Tape Strip Detector 3', 'Compression Load Cell 1', 'Pressure Transducer 1', 'Thermistor 1', 'Thermistor 2', 'Thermistor 3', 'Thermistor 4', 'Thermistor 5', 'Thermistor 6', 'Thermistor 7', 'Thermistor 8', 'Thermistor 9', 'Thermistor 10', 'Thermistor 11', 'Thermistor 12', 'Thermistor 13', 'Thermistor 14', 'Thermistor 15', 'Thermistor 16', 'Thermistor 17', 'Thermistor 18', 'Thermistor 19', 'Thermistor 20', 'Thermistor 21', 'Thermistor 22', 'Thermistor 23', 'Thermistor 24', 'Thermistor 25', 'Thermistor 26', 'Thermistor 27', 'Thermistor 28', 'Thermistor 29', 'Thermistor 30', 'Thermistor 31', 'Thermistor 32', 'Thermistor 33', 'Thermistor 34', 'Thermistor 35', 'Thermistor 36', 'Thermistor 37', 'Thermistor 38', 'Thermistor 39', 'Thermistor 40', 'Thermistor 41', 'Thermistor 42', 'Thermistor 43', 'Thermistor 44', 'Thermistor 45', 'Thermistor 46', 'Thermistor 47', 'Thermistor 48', 'Thermistor 49', 'Thermistor 50', 'Thermistor 51', 'Thermistor 52', 'Thermistor 53', 'Thermistor 54', 'Thermistor 55', 'Thermistor 56', 'Thermistor 57', 'Thermistor 58', 'Siren', 'Solid State Relay 1']
types = ["Sensor", "Actuator"]
locations = ["Boggie - Front left", "Brake Axle", "BPM2 - solid state relay", "Motor 8 - Middle Right"]

class Send(riffle.Domain):

    def onJoin(self):
        
        while True:
            self.publish("temp", {'module': random.choice(modules), 'data': str(random.random()), 'sensor': random.choice(sensors),'id': str(random.randrange(0,144)), 'type': random.choice(types), 'location': random.choice(locations)})
            time.sleep(2)

if __name__ == '__main__':
    riffle.SetFabric('ws://192.168.1.99:8000')
    domain = 'xs.node'
    Send(domain).join()
    exit()