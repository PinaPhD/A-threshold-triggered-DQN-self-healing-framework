import influxdb_client
from influxdb_client.client.query_api import QueryApi
import pandas as pd

# InfluxDB configuration
url = "http://192.168.0.7:8086"  # InfluxDB URL (Host Server)
token = "qkc2ZrwHen0ZzaPyBisN9E5bZYGNmhwO9R-ATu077_ieVy9ZqrhxqvHlzmn8zS2A5iCiBTGmSUM4hz9flPX6yg=="  # InfluxDB API Token
org = "Knowledge_Base"  # InfluxDB Organization
bucket = "Observe_Module_KB"  # Influx Bucket Name

# Initialize InfluxDB client
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

query_api = client.query_api()

# Define your query
query = f'''
from(bucket: "{bucket}")
  |> range(start: -1h)  // Adjust the time range as needed
  |> filter(fn: (r) => r._measurement == "port_stats")
'''

# Execute the query
tables = query_api.query(org=org, query=query)

# Process the results into a DataFrame
data = []
for table in tables:
    for record in table.records:
        data.append({
            "time": record.get_time(),
            "device": record["device"],
            "port": record["port"],
            "PacketsReceived": record["PacketsReceived"],
            "PacketsSent": record["PacketsSent"],
            "BytesReceived": record["BytesReceived"],
            "BytesSent": record["BytesSent"],
            "PacketsRxDropped": record["PacketsRxDropped"],
            "PacketsTxDropped": record["PacketsTxDropped"],
            "PacketsRxErrors": record["PacketsRxErrors"],
            "PacketsTxErrors": record["PacketsTxErrors"]
        })

df = pd.DataFrame(data)

# Print the DataFrame
print(df)

# Optionally, save to a CSV file
df.to_csv('port_statistics_from_influxdb.csv', index=False)
