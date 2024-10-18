import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Reading all the test cases
file_paths = [
    'TC1_data.csv', 'TC2_data.csv', 'TC3_data.csv', 
    'TC4_data.csv', 'TC5_data.csv', 'TC6_data.csv', 
    'TC7_data.csv', 'TC8_data.csv', 'TC9_data.csv'
]

# Colors for each packet loss bin range (one color per test case)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple']

# Number of bins for the packet loss values
num_bins = 10

# Width of each bar group (one bar per packet loss bin range)
bar_width = 0.1

# Initialize figure
plt.figure(figsize=(12, 8))

# Collect packet loss data from each file for binning
all_packet_loss = []

for file_path in file_paths:
    df = pd.read_csv(file_path)
    packet_loss = df.iloc[:, 2]  # Assuming packet loss is in the third column
    all_packet_loss.append(packet_loss)

# Compute common bins across all test cases (for packet loss ranges)
all_packet_loss_flat = np.concatenate(all_packet_loss)
bins = np.linspace(min(all_packet_loss_flat), max(all_packet_loss_flat), num_bins)

# Y-axis will represent the packet loss bin ranges
y_labels = [f'{bins[i]:.2f} - {bins[i + 1]:.2f}' for i in range(num_bins - 1)]

# X-axis positions for test cases 1 to 9
x_positions = np.arange(len(file_paths))

# Plot each test case as a grouped bar plot for each packet loss range
for idx, file_path in enumerate(file_paths):
    # Read the dataset
    df = pd.read_csv(file_path)
    
    # Assuming packet loss is in the third column
    packet_loss = df.iloc[:, 2]  
    
    # Calculate the count of values in each bin
    bin_counts, _ = np.histogram(packet_loss, bins=bins)
    
    # Offset y-axis positions for grouping bars by test case
    bin_y_positions = np.arange(num_bins - 1)
    
    # Plot the bar for this test case, using test case number as the x-axis
    plt.barh(bin_y_positions + idx * bar_width, bin_counts, height=bar_width, 
             color=colors[idx], label=f'Test Case {idx + 1}', edgecolor='black')

# Add labels, title, and legend
plt.xlabel('Number of Packet Loss Values', fontsize=18)
plt.ylabel('Packet Loss (%)', fontsize=18)
plt.title('Packet Loss Distribution Across Test Cases', fontsize=20)

# Set y-ticks and y-labels to represent packet loss bins
plt.yticks(np.arange(num_bins - 1) + bar_width * (len(file_paths) / 2 - 0.5), y_labels)

# Add a legend for the test cases
plt.legend(loc='upper right')

plt.grid(True)

# Show plot
plt.show()
