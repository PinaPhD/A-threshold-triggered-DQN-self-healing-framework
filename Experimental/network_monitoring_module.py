'''

@Author: Agrippina Mwangi
@Funding: InnoCyPES Project EU H2020 ITN
@Task: Secure self-healing module for software-defined Industrial OT Networks in extreme environments.
@Created in May 2024 (Orsted, Denmark)

'''

import requests
import prettytable as pt
from requests.auth import HTTPBasicAuth
from redis import Redis

# Configuration
onos_ip = '192.168.0.5'  # ONOS controller IP
auth_details = HTTPBasicAuth('onos', 'rocks')  # ONOS credentials
base_url = f'http://{onos_ip}:8181/onos/v1'
redis_host = 'localhost'  # Redis server IP
redis_port = 6379  # Redis server port

# Initialize Redis connection
redis_conn = Redis(host=redis_host, port=redis_port)

# Function to get network devices
def get_devices():
    response = requests.get(f"{base_url}/devices", auth=auth_details)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get links
def get_links():
    response = requests.get(f"{base_url}/links", auth=auth_details)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get topology
def get_topology():
    response = requests.get(f"{base_url}/topology", auth=auth_details)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to print and save to Redis in table format
def print_and_save_to_redis(data, name):
    table = pt.PrettyTable()
    if data and 'devices' in data:
        keys = data['devices'][0].keys()
        table.field_names = keys
        for item in data['devices']:
            table.add_row([item[key] for key in keys])
    elif data and 'links' in data:
        keys = data['links'][0].keys()
        table.field_names = keys
        for item in data['links']:
            table.add_row([item[key] for key in keys])
    elif data:
        keys = data.keys()
        table.field_names = keys
        table.add_row([data[key] for key in keys])

    print(f"{name} Table:")
    print(table)

    # Save to Redis
    redis_conn.set(name, str(table))

# Main function
def main():
    devices = get_devices()
    links = get_links()
    topology = get_topology()

    if devices:
        print_and_save_to_redis(devices, 'Devices')
    if links:
        print_and_save_to_redis(links, 'Links')
    if topology:
        print_and_save_to_redis(topology, 'Topology')

if __name__ == "__main__":
    main()
