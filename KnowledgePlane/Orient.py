#!/usr/bin/env python3

'''
	Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: July 2024
    ORIENT MODULE: Visualizing the network topology based on the current network state
'''


from Observe import current_network_state  #Loads the current network state from the OBSERVE Module
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

'''
    Visualize the network topology
'''

def visualize_network(devices, links, hosts):
    """Visualizes the network topology using NetworkX and Matplotlib."""
    G = nx.Graph()
    
    # Add device nodes
    for _, device in devices.iterrows():
        G.add_node(device['id'], label=device['id'], color='skyblue')
    
    # Add host nodes and their edges to devices
    for _, host in hosts.iterrows():
        host_id = host['id']
        for location in host['locations']:
            device_id = location['elementId']
            G.add_node(host_id, label=host_id, color='black')
            G.add_edge(host_id, device_id)
    
    # Add device-device edges
    for _, link in links.iterrows():
        src = link['src']['device']
        dst = link['dst']['device']
        G.add_edge(src, dst)
    
    # Get node colors
    node_colors = [G.nodes[node].get('color', 'skyblue') for node in G.nodes()]
    
    # Draw the network
    pos = nx.spring_layout(G)  # Layout for better visualization
    plt.figure(figsize=(15, 15))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=200, font_size=10, font_weight='bold', edge_color='gray')
    plt.title("Network Topology")
    plt.show()


'''
    Network traffic monitoring against system intents (captured as normalized thresholds)
'''

if __name__ == "__main__":
    # Get network state variables from file1.py
    devices, links, hosts, flows, port_stats, paths = current_network_state()
    
    #Visualize the network topology
    visualize_network(devices, links, hosts)