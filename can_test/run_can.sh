#!/bin/bash
sudo ifconfig can0 down
sudo ifconfig can1 down
# Set up CAN interfaces with specified bitrates
sudo ip link set can0 up type can bitrate 500000
sudo ip link set can1 up type can bitrate 125000
sudo ifconfig can0 txqueuelen 65536
sudo ifconfig can1 txqueuelen 65536

python3 log_can_test.py