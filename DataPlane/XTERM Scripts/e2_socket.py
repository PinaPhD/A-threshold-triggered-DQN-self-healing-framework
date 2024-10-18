#!/usr/bin/env python3

'''
    Designing the IIoT to Edge Computing Nodes data acquisition system
    Author: Agrippina W. Mwangi
    Created on: July 2024
    DATA PLANE: IIoT-Edge Computing Nodes 
'''


import socket
import json

def receive_sensor_data():
    server_address = ('10.0.1.51', 10100)  # IP address and port to listen on
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    try:
        while True:
            data, address = sock.recvfrom(4096)
            message = data.decode()
            sensor_data = json.loads(message)
            print(f'Received: {json.dumps(sensor_data, indent=4)} from {address}')
    except KeyboardInterrupt:
        print('Interrupted!')
    finally:
        sock.close()

if __name__ == '__main__':
    receive_sensor_data()
