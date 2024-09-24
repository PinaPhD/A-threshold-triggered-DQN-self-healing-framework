# -*- coding: utf-8 -*-

''' 
        Created on Wed Jul 24 14:13:22 2024
        @Project Title: Implementing self-healing autonomous software-defined OT networks in offshore wind power plants
        @Task: Observe-Orient-Decide-Act Closed Control Loop Self-healing framework
        @author: amwangi254
'''


import requests
import time
import logging
import pandas as pd
from time import strftime
from datetime import datetime
#import os
import json  # Import JSON module to convert dict to string
import mysql.connector
from mysql.connector import Error


'''
        ONOS SDN controller cluster interacting with the Knowledge Base
        Connecting to the primary SDN controller using a 8181 RESTful API based url and 
        BASE24 Authentication (Plain user/password credentials)
'''


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompting user for ONOS controller details
print("OBSERVE MODULE AS(n) OT Network Topology.\n Disclaimer: Press Enter if you wish to use the default configurations\n\n")
controller_ip = input("Enter the IP address of the ONOS controller (default is 192.168.0.6: )")
controller_ip = controller_ip if controller_ip else '192.168.0.6'
onos_base_url = f'http://{controller_ip}:8181/onos/v1'

username = input("Enter the username for ONOS controller (default is 'onos'): ")
username = username if username else 'onos'
password = input("Enter the password for ONOS controller (default is 'rocks'): ")
password = password if password else 'rocks'
onos_auth = (username, password)



def get_devices():
    """ 
        Fetches network devices from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/devices', auth=onos_auth)
        if response.status_code == 200:
            devices = response.json().get('devices', [])
            df = pd.DataFrame(devices)
            return df
        else:
            print(f"Failed to retrieve Network devices: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network devices: {e}")

def get_links():
    """ 
        Fetches network links from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/links', auth=onos_auth)
        if response.status_code == 200:
            links = response.json().get('links', [])
            df = pd.DataFrame(links)
            return df
        else:
            print(f"Failed to retrieve Network links: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network Links: {e}")

def get_hosts():
    """ 
        Fetches network hosts from the ONOS controller. 
    """

    try:
        response = requests.get(f'{onos_base_url}/hosts', auth=onos_auth)
        if response.status_code == 200:
            hosts = response.json().get('hosts', [])
            df = pd.DataFrame(hosts)
            return df
        else:
            print(f"Failed to retrieve Network hosts: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network hosts: {e}")

def get_flows():
    """ 
        Fetches flow rules from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/flows', auth=onos_auth)
        if response.status_code == 200:
            flows = response.json().get('flows', [])
            df = pd.DataFrame(flows)
            return df
        else:
            print(f"Failed to retrieve Network flows: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network flows: {e}")


def get_port_statistics():
    """ 
        Fetches port statistics from all devices in the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/statistics/ports', auth=onos_auth)
        if response.status_code == 200:
            port_stats = response.json().get('statistics', [])
            # Flatten the nested JSON structure for easier CSV writing
            flattened_stats = []
            for device in port_stats:
                device_id = device['device']
                for port in device['ports']:
                    port['device'] = device_id
                    flattened_stats.append(port)
            df = pd.DataFrame(flattened_stats)
            return df
        else:
            print(f"Failed to retrieve Port Statistics: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching network port statistics: {e}")



#For the paths
def get_devices_fp():
    response = requests.get(f'{onos_base_url}/devices', auth=onos_auth)
    return response.json()

# Function to get links
def get_links_fp():
    response = requests.get(f'{onos_base_url}/links', auth=onos_auth)
    return response.json()

#Determine the source to destination paths
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

# Generating the links between the source and destination paths
def src_to_dest_paths():
    devices = get_devices_fp()['devices']
    links = get_links_fp()['links']
    
    # Build adjacency list for the graph
    graph = {}
    for link in links:
        src = link['src']['device']
        dst = link['dst']['device']
        if src not in graph:
            graph[src] = []
        if dst not in graph:
            graph[dst] = []
        graph[src].append(dst)
        graph[dst].append(src)
    
    # Iterate over each pair of devices to find all paths
    device_ids = [device['id'] for device in devices]
    paths_list = []
    
    for i in range(len(device_ids)):
        for j in range(i + 1, len(device_ids)):
            source_device = device_ids[i]
            destination_device = device_ids[j]
            
            # Find all paths
            paths = find_all_paths(graph, source_device, destination_device)
            
            # Store paths
            for path in paths:
                paths_list.append({
                    'source': source_device,
                    'destination': destination_device,
                    'path': " -> ".join(path)
                })

    df_paths = pd.DataFrame(paths_list)
    return df_paths

'''
    Determining the switch utilization based on the port statistics captured from ONOS SDN Controller
'''

def current_network_state():
    devices = get_devices()
    links = get_links()
    hosts = get_hosts()
    flows = get_flows()
    port_stats = get_port_statistics()
    paths = src_to_dest_paths()
       
    return devices, links, hosts, flows, port_stats, paths


# Function to connect to MySQL database
def connect_to_mysql():
    
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Update with your MySQL host if different
            database='Orsted',  # Your database name
            user='root',  # Your MySQL username
            password='50acresIsinya'  # Your MySQL password
        )
        if connection.is_connected():
            logging.info('Connected to MySQL Database')
            return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL Database: {e}")
        return None


#Inserting Devices into mysql database
def insert_devices_to_mysql(devices_df, connection):
    
    
    """
    Inserts device data from the DataFrame into the devices table in MySQL.
    Skips the insertion if the ID already exists.
    """
    
    try:
        cursor = connection.cursor()

        replace_query = """
        REPLACE INTO devices 
        (id, type, available, role, mfr, hw, sw, serial, driver, chassisId, lastUpdate, humanReadableLastUpdate, annotations) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Iterate over the DataFrame and insert each row into the MySQL table
        for index, row in devices_df.iterrows():        

            # Data tuple for insertion
            data_tuple = (
                row.get('id', None),
                row.get('type', None),
                row.get('available', None) == 'TRUE',  # Convert to boolean
                row.get('role', None),
                row.get('mfr', None),
                row.get('hw', None),
                row.get('sw', None),
                row.get('serial', None),
                row.get('driver', None),
                row.get('chassisId', None),
                int(row.get('lastUpdate', 0)),  # Convert to int for BIGINT
                row.get('humanReadableLastUpdate', None),
                json.dumps(row.get('annotations', {}))
             )

            cursor.execute(replace_query, data_tuple)

        # Commit the transaction after inserting all rows
        connection.commit()

        logging.info("WFF OSS Devices inserted successfully into the MySQL database.")
    
    except mysql.connector.Error as e:
        logging.error(f"Failed to insert device data into MySQL table: {e}")
        connection.rollback()  # Rollback in case of error
    
    finally:
        cursor.close()
              
#Inserting Flows into mysql database        
def insert_flows_to_mysql(flows_df, connection):
    """
    Inserts flow data from the DataFrame into the flow table in the MySQL Orsted database.
    Assumes the 'flow' table has the following schema:
    | id (AUTO_INCREMENT) | tableId | appId | groupId | priority | timeout | isPermanent | 
    | deviceId | state | life | packets | bytes | liveType | lastSeen | treatment | selector |
    """
    
    try:
        cursor = connection.cursor()

        replace_query = """
        REPLACE INTO flows 
        (id, tableId, appId, groupId, priority, timeout, isPermanent, deviceId, state, life, packets, bytes, liveType, lastSeen, treatment, selector) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Iterate over the DataFrame and insert each row into the MySQL table
        for index, row in flows_df.iterrows():
           
            data_tuple = (
                row.get('id', None),
                row.get('tableId', None),
                row.get('appId', None),
                row.get('groupId', None),
                row.get('priority', None),
                row.get('timeout', None),
                row.get('isPermanent', None),
                row.get('deviceId', None),
                row.get('state', None),
                row.get('life', None),
                row.get('packets', None),
                row.get('bytes', None),
                row.get('liveType', None),
                row.get('lastSeen', None),
                json.dumps(row.get('treatment', {})),  # Convert dict to JSON string
                json.dumps(row.get('selector', {}))   # Convert dict to JSON string
            )
            
            cursor.execute(replace_query, data_tuple)

        # Commit the transaction after inserting all rows
        connection.commit()

        logging.info("SDNC flows inserted successfully into the MySQL database.")
    
    except mysql.connector.Error as e:
        logging.error(f"Failed to insert flow data into MySQL table: {e}")
        connection.rollback()  # Rollback in case of error
    
    finally:
        cursor.close()

#Inserting Hosts into mysql database
def insert_hosts_to_mysql(hosts_df, connection):
    """
    Inserts or replaces data into the hosts table in MySQL.
    If a row with the same id already exists, it will be replaced.
    """
    try:
        cursor = connection.cursor()

        replace_query = """
        REPLACE INTO hosts 
        (id, mac, vlan, innerVlan, outerTpid, configured, ipAddresses, locations) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Iterate over the DataFrame and insert or replace each row into the MySQL table
        for index, row in hosts_df.iterrows():
            # Parse the ipAddresses and locations fields to JSON
            ipAddresses = json.dumps(row.get('ipAddresses', []))
            locations = json.dumps(row.get('locations', []))

            # Data tuple for insertion
            data_tuple = (
                row.get('id', None),
                row.get('mac', None),
                row.get('vlan', None),
                row.get('innerVlan', None),
                row.get('outerTpid', None),
                row.get('configured', None),
                ipAddresses,
                locations
            )
            
            cursor.execute(replace_query, data_tuple)

        # Commit the transaction after inserting all rows
        connection.commit()

        logging.info("WFF OSS hosts inserted successfully into the MySQL database.")
    
    except mysql.connector.Error as e:
        logging.error(f"Failed to insert flow data into MySQL table: {e}")
        connection.rollback()  # Rollback in case of error
    
    finally:
        cursor.close()

#Inserting Ports into mysql database
def insert_ports(ports_df, connection):
    """
    Inserts port data from the DataFrame into the ports table in MySQL.
    """
    try:
        cursor = connection.cursor()

        insert_query = """
        REPLACE INTO ports (port_identifier, device_name, port_number)
        VALUES (%s, %s, %s)
        """
        
        # Iterate over the DataFrame and insert each row
        for index, row in ports_df.iterrows():
            data_tuple = (
                row['port_identifier'],
                row['device_name'],
                row['port_number']
            )
            cursor.execute(insert_query, data_tuple)

        # Commit the transaction after inserting all rows
        connection.commit()

        logging.info("WFF OSS Network Device ports inserted successfully in the MySQL database.")
    
    except mysql.connector.Error as e:
        logging.error(f"Failed to insert port data: {e}")
        connection.rollback()
    
    finally:
        cursor.close()

#Inserting Network Links into mysql database
def insert_network_links(network_links_df, connection):
    """
    Inserts network link data from the DataFrame into the network_links table in MySQL.
    """
    try:
        cursor = connection.cursor()

        insert_query = """
        REPLACE INTO network_links (link_id, src_port_identifier, dest_port_identifier)
        VALUES (%s, %s, %s)
        """
        
        # Iterate over the DataFrame and insert each row
        for index, row in network_links_df.iterrows():
            data_tuple = (
                row['link_id'],
                row['src_port_identifier'],
                row['dest_port_identifier']
            )
            cursor.execute(insert_query, data_tuple)

        # Commit the transaction after inserting all rows
        connection.commit()

        logging.info("WFF OSS network links inserted successfully in the MySQL database.")
    
    except mysql.connector.Error as e:
        logging.error(f"Failed to insert network link data: {e}")
        connection.rollback()
    
    finally:
        cursor.close()

def insert_link_port_stats(link_port_stats_df, connection):
    """
    Inserts link port statistics from the DataFrame into the link_port_stats table in MySQL.
    """
    try:
        cursor = connection.cursor()

        insert_query = """
        REPLACE INTO link_port_stats (link_stats_id, link_id, timestamp, PacketsReceived, PacketsSent, 
                                      BytesReceived, BytesSent, PacketsRxDropped, PacketsTxDropped, 
                                      PacketsRxErrors, PacketsTxErrors)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Iterate over the DataFrame and insert each row
        for index, row in link_port_stats_df.iterrows():
            data_tuple = (
                row['link_stats_id'],
                row['link_id'],
                row['timestamp'],
                row['PacketsReceived'],
                row['PacketsSent'],
                row['BytesReceived'],
                row['BytesSent'],
                row['PacketsRxDropped'],
                row['PacketsTxDropped'],
                row['PacketsRxErrors'],
                row['PacketsTxErrors']
            )
            cursor.execute(insert_query, data_tuple)

        # Commit the transaction after inserting all rows
        connection.commit()

        logging.info("link port statistics inserted successfully in the MySQL database.")
    
    except mysql.connector.Error as e:
        logging.error(f"Failed to insert link port statistics: {e}")
        connection.rollback()
    
    finally:
        cursor.close()


if __name__ == "__main__":
    try:
        # Reading the current network state
        devices, links, hosts, flows, port_stats, paths = current_network_state()

        '''
            Accessing the network links and port statistics to determine the network utilization
        '''
        # Create Port DataFrame
        ports = []
        for index, row in links.iterrows():
            src_device, src_port = row['src']['device'], row['src']['port']
            dest_device, dest_port = row['dst']['device'], row['dst']['port']
            ports.append({'port_identifier': f'{src_device}_{src_port}', 'device_name': src_device, 'port_number': src_port})
            ports.append({'port_identifier': f'{dest_device}_{dest_port}', 'device_name': dest_device, 'port_number': dest_port})
        
        port_df = pd.DataFrame(ports).drop_duplicates().reset_index(drop=True)

        # Create Network Links DataFrame
        network_links = []
        for index, row in links.iterrows():
            src_device, src_port = row['src']['device'], row['src']['port']
            dest_device, dest_port = row['dst']['device'], row['dst']['port']
            link_id = f'{src_device}_{src_port}_to_{dest_device}_{dest_port}'
            src_port_identifier = f'{src_device}_{src_port}'
            dest_port_identifier = f'{dest_device}_{dest_port}'
            network_links.append({'link_id': link_id, 'src_port_identifier': src_port_identifier, 'dest_port_identifier': dest_port_identifier})
        
        network_links_df = pd.DataFrame(network_links)

        # Initialize DataFrame to store link port statistics
        link_port_stats_df = pd.DataFrame(columns=['link_stats_id', 'link_id', 'timestamp', 'PacketsReceived', 'PacketsSent', 'BytesReceived', 'BytesSent', 'PacketsRxDropped', 'PacketsTxDropped', 'PacketsRxErrors', 'PacketsTxErrors'])
        
        
        '''
            Saving data into the mysql Database
        '''
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # ISO 8601 format
        # Connect to MySQL Database
        mysql_conn = connect_to_mysql()
        
        if mysql_conn:
            
            while True:
                # Insert devices into the MySQL table
                insert_devices_to_mysql(devices, mysql_conn)
                
                # Insert the flow data into the MySQL flow table
                insert_flows_to_mysql(flows, mysql_conn)
                #print(f'\nInserting flows to the MySQL flows table at: {timestamp}')
                
                # Insert hosts data into the MySQL table
                insert_hosts_to_mysql(hosts, mysql_conn)
                
                #Insert ports into the MySQL table
                insert_ports(port_df, mysql_conn)

                #Insert network links into the MySQL table
                insert_network_links(network_links_df, mysql_conn)

                #Insert the link statistics into the MySQL table
                insert_link_port_stats(link_port_stats_df, mysql_conn)

                
                # Send data samples every second -- before the next iteration
                time.sleep(10)
            
    except KeyboardInterrupt:
        
        # Close MySQL connection when stopping the script
        if mysql_conn and mysql_conn.is_connected():
            mysql_conn.close()
            logging.info('MySQL connection closed.')
        logging.info('Process interrupted by the network engineer.')
        
        
       