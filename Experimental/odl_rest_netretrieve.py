import requests
from requests.auth import HTTPBasicAuth

# Set your OpenDaylight controller's IP address and port
controller_ip = "192.168.181.132"
controller_port = "8181"

# Set your OpenDaylight credentials
username = "admin"
password = "admin"

# Construct the URL for retrieving the network topology
url = f"http://{controller_ip}:{controller_port}/restconf/operational/network-topology:network-topology"

# Send an HTTP GET request to the URL
response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={"Accept": "application/json"})

# Check if the request was successful
if response.status_code == 200:
    topology_data = response.json()

    # Extract nodes and links from topology data
    nodes = topology_data.get("network-topology", {}).get("topology", [])[0].get("node", [])
    links = topology_data.get("network-topology", {}).get("topology", [])[0].get("link", [])

    # Print the network topology in a tabular format
    print("Node ID\t\tNode Type\tConnected Links")
    print("=" * 50)
    for node in nodes:
        node_id = node.get("node-id", "")
        node_type = node.get("node-type", "")
        connected_links = [link.get("link-id") for link in links if node_id in link.get("source", {}).get("source-node", "")]
        connected_links_str = ", ".join(connected_links)
        print(f"{node_id}\t\t{node_type}\t\t{connected_links_str}")
else:
    print(f"Failed to retrieve network topology. Status code: {response.status_code}")

