import requests

# ONOS REST API base URL
onos_base_url = 'http://192.168.0.6:8181/onos/v1'

# REST API authentication
auth = ('onos', 'rocks')  # Default credentials

# Function to get devices
def get_devices():
    response = requests.get(f'{onos_base_url}/devices', auth=auth)
    return response.json()

# Function to get links
def get_links():
    response = requests.get(f'{onos_base_url}/links', auth=auth)
    return response.json()

# Function to find all paths using DFS
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

# Main function
def main():
    devices = get_devices()['devices']
    links = get_links()['links']
    
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
    
    for i in range(len(device_ids)):
        for j in range(i + 1, len(device_ids)):
            source_device = device_ids[i]
            destination_device = device_ids[j]
            
            # Find all paths
            paths = find_all_paths(graph, source_device, destination_device)
            
            # Print paths
            print(f"Paths between {source_device} and {destination_device}:")
            for path in paths:
                print(" -> ".join(path))
            print()

if __name__ == '__main__':
    main()
