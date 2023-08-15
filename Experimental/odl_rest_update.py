import requests
from requests.auth import HTTPBasicAuth

# Set your OpenDaylight controller's IP address and port
controller_ip = "192.168.181.133"
controller_port = "8181"

# Set your OpenDaylight credentials
username = "admin"
password = "admin"

# Set the flow ID you want to update
flow_id = "L2switch-10"

# Construct the URL for the specific flow entry
url = f"http://{controller_ip}:{controller_port}/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/{flow_id}"

# Construct the JSON payload for the updated flow entry
updated_flow_entry = {
    "flow": {
        "id": flow_id,
        "priority": 200,  # Update the priority to your desired value
        # You can also modify other attributes and actions here
    }
}

# Send an HTTP PUT request to update the flow entry
response = requests.put(url, json=updated_flow_entry, auth=HTTPBasicAuth(username, password), headers={"Content-Type": "application/json"})

# Check if the request was successful
if response.status_code == 200:
    print(f"Flow entry {flow_id} updated successfully.")
else:
    print(f"Failed to update flow entry {flow_id}. Status code: {response.status_code}")

