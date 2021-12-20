#! /usr/bin/python -m pipenv run python -i


import time
import serial
import requests


# Open serial port
ser = serial.Serial('COM5', 9600, timeout=0.5)  # rtscts=1

# Set mode as CONTROLLER
ser.write('++mode 1\n'.encode())

# Set HP33120A address
ser.write('++addr 13\n'.encode())

# Turn off read-after-write to avoid 'Query Unterminated' errors
ser.write('++auto 1\n'.encode())

# ?? Do not append CR or LF to GPIB data
ser.write('++eos 3\n'.encode())

# Assert EOI with last byte to indicate end of data
ser.write('++eoi 1\n'.encode())

# ser.close()


def send(datum, value):
    payload = '{0!s} value={1!s}'.format(datum, value)
    try:
        r = requests.post('http://192.168.57.103:8086/write?db=VHz', data=payload)
        # print(r.status_code)
    except requests.exceptions.ConnectionError:
        print('Failed to Connect to InfluxDB')


while True:
    time.sleep(1)
    # Hz = float(inst.query(':FNC:FRQ?'))
    # V = float(inst.query(':FNC:VLT?'))
    ser.readall()
    ser.write(b':FNC:VLT?\n \r')
    time.sleep(0.1)
    # print(ser.readall())
    try:
        V = float((ser.readall().strip()).decode())

        ser.readall()
        ser.write(b':FNC:FRQ?\n \r')
        time.sleep(0.1)
        # print(ser.readall())
        Hz = float((ser.readall().strip()).decode())
        # Hz = 50.0
        print('{} Volts AC, {} Hz'.format(V, Hz))
        if V > 64:
            send('Voltage', V)
        send('Frequency', Hz)
    except ValueError:
        pass


'''
>>> ser.readall() ; ser.write(b'++addr\r') ; time.sleep(0.1) ; ser.readall()
b''
7
b'13\r\n'

>>> ser.readall() ; ser.write(b':FNC:VLT?\n \r') ; time.sleep(0.1) ; ser.readall().strip()
b''
12
b'2.394E2'
'''
