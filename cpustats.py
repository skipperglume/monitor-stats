# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# """
# Copyright (c) 2012, Rui Carmo
# Description: Utility functions for retrieving CPU statistics
# License: MIT (see LICENSE.md for details)
# """

# import logging
# import time

# log = logging.getLogger()


# def stats():
#     """Retrieves all CPU counters"""
#     cpu = open('/proc/stat','r').readlines()[0]
#     return map(float,cpu.split()[1:5])


# def usage(interval=0.1):
#     """Estimates overall CPU usage during a short time interval"""
#     t1 = stats()
#     time.sleep(interval)
#     t2 = stats() 
#     print(t1)
#     print(t2)
#     delta = [t2[i] - t1[i] for i in range(len(t1))]
#     try:
#         return 1.0 - (delta[-1:].pop()/(sum(delta)*1.0))
#     except: 
#         return 0.0


# def freqency(cpu='cpu0'):
#     """Retrieves the current CPU speed in MHz - for a single CPU"""
#     return float(open('/sys/devices/system/cpu/%s/cpufreq/scaling_cur_freq' % cpu,'r').read().strip())/1000.0


# def temperature():
#     """Retrieves the current CPU core temperature in degrees Celsius - tailored to the Raspberry Pi"""
#     return float(open('/sys/class/thermal/thermal_zone0/temp','r').read().strip())/1000.0


# if __name__ == '__main__':


import time
import signal
import sys

def read_proc_stat():
    """
    Reads the /proc/stat file and returns a list of CPU times.
    """
    with open('/proc/stat', 'r') as f:
        lines = f.readlines()
    # The first line starts with 'cpu' and contains the aggregate CPU stats
    cpu_line = lines[0]
    return list(map(int, cpu_line.split()[1:]))  # Ignore the 'cpu' keyword

def calculate_cpu_usage(prev_idle, prev_total, curr_idle, curr_total):
    """
    Calculate the CPU usage between two time intervals.
    """
    idle_diff = curr_idle - prev_idle
    total_diff = curr_total - prev_total
    usage = (total_diff - idle_diff) / total_diff * 100
    return usage


def graceful_exit(signal_received, frame):
    print("\nGracefully exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)

def monitor_cpu(interval=1):
    """
    Monitor and print CPU usage at regular intervals.
    """
    prev_stats = read_proc_stat()
    prev_idle, prev_total = prev_stats[3], sum(prev_stats)
    print(prev_stats)
    try:
        while True:
            time.sleep(interval)
            curr_stats = read_proc_stat()
            curr_idle, curr_total = curr_stats[3], sum(curr_stats)

            cpu_usage = calculate_cpu_usage(prev_idle, prev_total, curr_idle, curr_total)

            print(f"CPU Usage: {cpu_usage:.2f}%")

            # Update previous stats
            prev_idle, prev_total = curr_idle, curr_total
    except KeyboardInterrupt:
        gracefulExit(None, None)
if __name__ == "__main__":
    monitor_cpu(1)  # Monitor CPU every 1 second
    # logging.basicConfig(level=logging.DEBUG)
    # log.debug('CPU usage: %f' % usage())
    # log.debug('CPU frequency: %f' % freqency())
    # log.debug('CPU temperature: %f' % temperature())