#!/usr/bin/env python3

import sys
import serial
from serial.tools.list_ports import comports

import statistics
import time

def dump_port_list():
 if comports:
  print('\n--- Available ports:')
  for port, desc, hwid in sorted(comports()):
   print('--- %-20s %s' % (port, desc))

def set_port():
 print('--- Enter port name: ')
 try:
  port = sys.stdin.readline().strip()
 except KeyboardInterrupt:
  port = None
 return(port)




def main(argv):
    """."""
    ser = serial.Serial('COM14', 115200, timeout=2)
    readings = 48
    meas = []
    print('Starting')
    
    while [True]:
        # time.sleep(0.005)  # prevent it from being a pu
        sample = ser.readline().strip()
        if sample != b'':
        #    if isinstance(sample, int):
            meas.append(int(sample))

        if len(meas) > readings:
            meas.pop(0)  # remove item at index 0
            print(int(statistics.mean(meas)))

    ser.close()


if __name__ == "__main__":
    try:
        dump_port_list()
        main(sys.argv)
    except KeyboardInterrupt:
        print('Received Ctrl-c')
