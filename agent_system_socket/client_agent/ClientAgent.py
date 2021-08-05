import socket
from select import *
import sys
import bluetooth
import json
import SensorDeliverer as sd
import ActuatorManager as am

if __name__ == "__main__":
    file_path = 'config.json'
    with open(file_path, "r") as fj:
        fd = json.load(fj)
        HOST = fd['SERVER_IP']
        PORT_SENSOR = fd['SERVER_PORT_SENSOR']
        PORT_ACTUATOR = fd['SERVER_PORT_ACTUATOR']
        BT_ADDR = fd['BT_ADDR']
        BT_PORT = fd['BT_PORT']
        SYSTEM_ID = fd['SYSTEM_ID']

    print("System ID : ", SYSTEM_ID)
    print("Server Host Sensor : ", HOST, " | Port : ", PORT_SENSOR)
    print("Server Host Actuator : ", HOST, " | Port : ", PORT_ACTUATOR)
    print("Bluetooth Address : ", BT_ADDR, "Port : ", BT_PORT)

    # Bluetooth Socket
    bt_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    bt_socket.connect((BT_ADDR,BT_PORT))
    
    sensor = sd.SensorDeliverer(bt_socket, HOST, PORT_SENSOR, SYSTEM_ID)
    actuator = am.ActuatorManager(bt_socket, HOST, PORT_ACTUATOR, SYSTEM_ID)
    
    sensor.start()
    actuator.start()
    
    sensor.join()
    actuator.join()
    
    bt_socket.close()

