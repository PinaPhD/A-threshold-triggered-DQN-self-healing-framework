#!/usr/bin/env python3

'''
    Designing the IIoT to Edge Computing Nodes data acquisition system
    Author: Agrippina W. Mwangi
    Created on: July 2024
    DATA PLANE: IIoT-Edge Computing Nodes 
'''


import socket
import logging
from datetime import datetime

# Setup logging
log_file = "/tmp/server_socket.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

server_ip = "10.0.1.54"  # Listen to R5 (LDAQ)
server_port = 54000  # Port number to listen on
end_date = datetime(2024, 10, 31)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)  # Allow up to 5 clients to connect

logging.info("Server listening on %s:%d", server_ip, server_port)

try:
    while datetime.now() <= end_date:
        client_socket, client_address = server_socket.accept()
        logging.info("Connection from %s:%d", client_address[0], client_address[1])
        
        while datetime.now() <= end_date:
            data = client_socket.recv(1024)
            if not data:
                break
            logging.info("Received data: %s", data.decode())
        
        client_socket.close()
        logging.info("Client %s disconnected", client_address[0])
finally:
    server_socket.close()
    logging.info("Server stopped")
