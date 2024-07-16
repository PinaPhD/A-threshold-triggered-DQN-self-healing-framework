# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:01:26 2024

@author: amwangi254
"""

# subscriber_socket.py
import socket
import logging
from datetime import datetime

# Setup logging
log_file = "/tmp/subscriber_socket.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

server_ip = "10.0.1.50"  # IP address of this host (e2)
server_port = 50000  # Port number to listen on

end_date = datetime(2024, 10, 31)

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    logging.info("Listening on %s:%d", server_ip, server_port)
    
    client_socket, client_address = server_socket.accept()
    logging.info("Connection from %s:%d", client_address[0], client_address[1])
    
    while datetime.now() <= end_date:
        data = client_socket.recv(1024)
        if not data:
            break
        logging.info("Received data: %s", data.decode())
    logging.info("Reached the end date. Stopping the script.")
except Exception as e:
    logging.error("An error occurred: %s", str(e))
finally:
    client_socket.close()
    server_socket.close()
    logging.info("Disconnected from client")
