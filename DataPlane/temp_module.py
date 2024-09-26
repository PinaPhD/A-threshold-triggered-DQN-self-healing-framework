# -*- coding: utf-8 -*-
"""
    Created on Tue Sep 05 14:11:18 2024
    @Main Contributor:  León Navarro-Hilfiker
    @Contributor: Agrippina Mwangi
"""
import mysql.connector
import pandas as pd


# Set the threshold for bytes received
THRESHOLD = 190000000

# Function to fetch the latest values from the view
def fetch_latest_device_statistics():
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",        # e.g. "localhost" or IP address
        user="root",    # e.g. "root"
        password="50acresIsinya",# e.g. "password"
        database="Orsted" # Name of the database containing the view
    )
    
    # Create a cursor to execute queries
    cursor = conn.cursor(dictionary=True)

    # SQL query to fetch the latest values (most recent timestamp)
    query = """
    SELECT *
    FROM port_statistics_device_agg
    WHERE timestamp = (SELECT MAX(timestamp) FROM port_statistics_device_agg)
    """
    
    cursor.execute(query)
    
    # Fetch all rows and load them into a Pandas DataFrame
    rows = cursor.fetchall()
    data = pd.DataFrame(rows)

    # Close the connection
    cursor.close()
    conn.close()

    return data

# Function to check switch utilization against the threshold
def check_switch_utilization(data):
    # Check which devices have exceeded the threshold
    data['exceeds_threshold'] = data['total_bytesReceived'] > THRESHOLD

    # Calculate the percentage of utilization against the threshold
    data['utilization_percentage'] = (data['total_bytesReceived'] / THRESHOLD) * 100

    # Filter the devices that exceeded the threshold
    exceeded_devices = data[data['exceeds_threshold']]

    return exceeded_devices[['device', 'total_bytesReceived', 'utilization_percentage']]
# Main execution
if __name__ == "__main__":
    # Fetch the latest statistics from the view
    latest_device_statistics = fetch_latest_device_statistics()

    # Check for devices that exceed the threshold and calculate utilization
    exceeded_device_stats = check_switch_utilization(latest_device_statistics)

    # Output the result as a Pandas DataFrame
    #print(exceeded_device_stats)
    
    
