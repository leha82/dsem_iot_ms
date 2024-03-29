import socket
from select import *
import sys
from time import sleep
import bluetooth
import json
import SensorDeliverer as sd
import ActuatorManager as am

frontstr = "Client >> "

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
    print("System ID Type : ", type(SYSTEM_ID))
    print("Server Host Sensor : ", HOST, " | Port : ", PORT_SENSOR)
    print("Server Host Actuator : ", HOST, " | Port : ", PORT_ACTUATOR)
    print("Bluetooth Address : ", BT_ADDR, "Port : ", BT_PORT)

    loop = True

    while loop:
        # Bluetooth Socket
        try :
            print(frontstr, "Bluetooth connecting ... ", end="")
            bt_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            bt_socket.connect((BT_ADDR,BT_PORT))
            print("Success!!")

            sensor = sd.SensorDeliverer(bt_socket, HOST, PORT_SENSOR, SYSTEM_ID)
            actuator = am.ActuatorManager(bt_socket, HOST, PORT_ACTUATOR, SYSTEM_ID)
            
            sensor.start()
            actuator.start()
            
            sensor.join()
            actuator.join()
        except KeyboardInterrupt:
            print(frontstr, "ClientAgent is stopped.")
        except Exception as e :
            print(frontstr, "Error is occured : ", e)

        bt_socket.close()
        print(frontstr, "Bluetooth socket closed.")
        print(frontstr, "Sleep 5 sec for next connection.")
        sleep(5)


