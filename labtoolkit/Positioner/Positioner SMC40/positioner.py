import binascii
import math
import struct
import time

from pprint import pprint

import serial
from serial.tools import list_ports

	
for each in list_ports.comports():
    print('{}\t\t{}'.format(each.device, each.description))
port = input('Serial Port? : ')
# port = 'COM7'

with serial.Serial(port, 9600, timeout=1, bytesize=8, parity='N', stopbits=1) as ser:
    while ser.isOpen():
        ser.write(b'ID')
        print(ser.readline())
        # self.write('XMN{}'.format(int(stepsize*100)))  # 100 is 1 degree
        # self.write('D+')  # Clockwise
        # self.write('D-')  # Anti-Clockwise
        # self.write('XGH')  # Go Home
        # self.write('@0')  # Init?
        # 'XMC'  # Complete?
        
