# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 05:54:47 2024

@author: IAN CARTER KULANI
"""

import psutil
import socket
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from scapy.all import *
import time
import seaborn as sns
import requests

# Function to monitor CPU and Memory usage
def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    mem_usage = memory_info.percent
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent / (1024 * 1024)  # in MB
    bytes_recv = net_io.bytes_recv / (1024 * 1024)  # in MB
    return cpu_usage, mem_usage, bytes_sent, bytes_recv

# Function to get the round-trip time for an IP address
def get_rtt(ip_address):
    try:
        # Simple TCP connection test for RTT
        start_time = time.time()
        sock = socket.create_connection((ip_address, 80), timeout=2)
        sock.close()
        rtt = (time.time() - start_time) * 1000  # in milliseconds
        return rtt
    except socket.error:
        return None

# Function to visualize the data
def plot_data(cpu_usage, mem_usage, bytes_sent, bytes_recv, rtt):
    # Create the pie chart for CPU and Memory usage
    labels = ['CPU Usage', 'Memory Usage']
    sizes = [cpu_usage, mem_usage]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("CPU and Memory Usage")
    plt.show()

    # Create the bar chart for Network Traffic
    labels = ['Bytes Sent (MB)', 'Bytes Received (MB)']
    sizes = [bytes_sent, bytes_recv]
    plt.bar(labels, sizes)
    plt.title("Network Traffic")
    plt.show()

    # Display RTT
    if rtt is not None:
        print(f"Round Trip Time to IP: {rtt:.2f} ms")
    else:
        print("Unable to calculate RTT")

# Function to handle user input and display the data
def monitor():
    ip_address = entry_ip.get()  # Get IP address from user input
    if not ip_address:
        messagebox.showerror("Input Error", "Please enter a valid IP address!")
        return

    # Get system stats
    cpu_usage, mem_usage, bytes_sent, bytes_recv = get_system_stats()

    # Get round-trip time (RTT)
    rtt = get_rtt(ip_address)

    # Plot the data
    plot_data(cpu_usage, mem_usage, bytes_sent, bytes_recv, rtt)

# Function for GUI
def create_gui():
    window = tk.Tk()
    window.title("Northen Malawi Internet Exchange Point")

    # Create input field for IP address
    tk.Label(window, text="Enter IP address to monitor:").pack(pady=10)
    global entry_ip
    entry_ip = tk.Entry(window, width=20)
    entry_ip.pack(pady=10)

    # Button to start monitoring
    monitor_button = tk.Button(window, text="Start Monitoring", command=monitor)
    monitor_button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
