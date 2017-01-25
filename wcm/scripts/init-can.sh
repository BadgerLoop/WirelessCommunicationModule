#!/usr/bin/env bash
echo "i 0x011C e" > /dev/pcan0
echo "i 0x011C e" > /dev/pcan1
echo "i 0x011C e" > /dev/pcan2
echo "i 0x011C e" > /dev/pcan3

ifconfig can0 up
ifconfig can1 up
ifconfig can2 up
ifconfig can3 up