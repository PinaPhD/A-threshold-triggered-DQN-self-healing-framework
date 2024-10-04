# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:56:26 2024

@author: amwangi254
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# Load the cleaned dataset
file_path = 'switch_temp_Thursday.csv'  # Update this with the correct path to your cleaned file

# Check if the file path is correct and handle errors
try:
    data_cleaned = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    raise

# Convert the 'timestamp' to datetime for proper time-based analysis
data_cleaned['timestamp'] = pd.to_datetime(data_cleaned['timestamp'])

# Set the 'timestamp' as the index for easier plotting
data_cleaned.set_index('timestamp', inplace=True)

# Main Plot
plt.figure(figsize=(20, 6))

# Group by device and plot each device's temperature over time
for device, group in data_cleaned.groupby('device'):
    plt.plot(group.index, group['temperature'], label=device)

# Set xticks to every 15 seconds (if you want more frequent ticks)
plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=15))  # Show xticks every 15 seconds for the main plot
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # Format as Hour:Minute:Second

# Add labels and title
plt.xlabel('Time(HH:MM:SS)', fontsize=22)
plt.ylabel('Temperature (°C)', fontsize=22)
plt.title('Time series plot for switch temperatures for varied test case scenarios', fontsize=22)

# Improve the legend by splitting into columns
plt.legend(title="Devices", bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2)
plt.xticks(rotation=45)
plt.ylim([16, 28])  # Adjusting the y-axis to zoom in the plots a bit more
plt.grid()

# Create an inset for zoomed-in section
# Set the position relative to the main plot (loc=1 means upper right)
ax_inset = inset_axes(plt.gca(), width="30%", height="40%", 
                      bbox_to_anchor=(0.3, 0.15, 0.65, 0.5), 
                      bbox_transform=plt.gca().transAxes)

# Plot the zoomed section in the inset
for device, group in data_cleaned.groupby('device'):
    ax_inset.plot(group.index, group['temperature'], label=device)

# Set the limits for the zoomed-in inset
xmin = pd.to_datetime('2024-10-03 11:47:45')  # start time
xmax = pd.to_datetime('2024-10-03 11:51:30')  # end time
ymin = 25  # Example minimum temperature
ymax = 27  # Example maximum temperature
ax_inset.set_xlim([xmin, xmax])
ax_inset.set_ylim([ymin, ymax])

# Set xticks for the inset
ax_inset.xaxis.set_major_locator(mdates.SecondLocator(interval=30))  # Show xticks every 30 seconds in the inset
ax_inset.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # Format as Hour:Minute:Second
ax_inset.tick_params(axis='x', rotation=45)

# Add grid and labels for the inset
ax_inset.grid()
ax_inset.set_title("Test Cases TC6 and TC9", fontsize=14)
ax_inset.set_xlabel('Time(HH:MM:SS)', fontsize=12)
ax_inset.set_ylabel('Temp (°C)', fontsize=12)

# Highlight the zoomed section in the main plot with lines
mark_inset(plt.gca(), ax_inset, loc1=2, loc2=4, fc="none", ec="red", lw=0.5)

# Show the plot with inset
plt.show()
