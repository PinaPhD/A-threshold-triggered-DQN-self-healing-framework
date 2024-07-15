#!/usr/bin/env python3

'''
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: July 2024
    ORIENT MODULE: Provides insights into the network traffic and triggers the DECIDE module
    when the QoS/SLA thresholds are exceeded.
'''


import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#Function to get the latest timestamped folder
def read_network_state(base_path):
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    folders.sort(reverse=True)
    if folders:
        return os.path.join(base_path, folders[0])
    return None

# Function to create a non-oriented graph from devices and links
def create_network_graph(devices, links):
    G = nx.Graph()

    # Add devices as nodes
    for index, device in devices.iterrows():
        G.add_node(device['id'], label=device['id'])

    # Add links as edges
    for index, link in links.iterrows():
        src = link['src_device']
        dst = link['dst_device']
        G.add_edge(src, dst)

    return G

# Function to draw the network graph
def draw_network_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2500, edge_color='gray', font_size=10, font_weight='bold')
    plt.title('Network Topology')
    plt.show()

# Function to create a topology matrix from the graph
def create_topology_matrix(G):
    matrix = nx.adjacency_matrix(G).todense()
    return pd.DataFrame(matrix, index=G.nodes(), columns=G.nodes())

# Main function to read CSV files and display network graph
if __name__ == "__main__":
    base_path = '.'

    # Get the latest timestamped folder
    current_network_state = read_network_state(base_path)
    if current_network_state:
        print(f"Reading data from the latest folder: {current_network_state}")

        # Reading CSV files
        devices = pd.read_csv(os.path.join(current_network_state, 'devices.csv'))
        links = pd.read_csv(os.path.join(current_network_state, 'links.csv'))
        
        # Extract relevant information from links DataFrame
        links['src_device'] = links['src'].apply(lambda x: eval(x)['device'])
        links['dst_device'] = links['dst'].apply(lambda x: eval(x)['device'])

        # Create and draw network graph
        G = create_network_graph(devices, links)
        draw_network_graph(G)

        # Create and display the topology matrix
        topology_matrix = create_topology_matrix(G)
        print("Topology Matrix:")
        print(topology_matrix)
    else:
        print("Orient Module could not read the current network state.\\Try Again :-)")

