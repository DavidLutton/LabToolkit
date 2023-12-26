import sys
import serial

import serial.tools.list_ports
import numpy as np
import pyvisa

rm = pyvisa.ResourceManager('@py')

inst = rm.open_resource(
    'TCPIP::127.0.0.1::10000::SOCKET',
    read_termination='\r\n',
    write_termination='\n',
    timeout=500
)
IDN = inst.query('*IDN?')
print(f'Connected to {IDN}')
# inst.close()

for port in serial.tools.list_ports.comports():
    print(f'{port.name}  == {port.description}')

port = input('Serial COM port? : ')
ser = serial.Serial(port, 4800, timeout=2)

# ser.readline() # read the init feedback
# b'\x13\x11\x13\x11\x13\x11\x13\x11\x13\x11'
print(f'Emulating EMC-20 probe via {port}')
print(f'Ready for querys')

while [ True ]:
    sample = ser.readline()
    # print(sample)
    if sample == b'M\n':
        # out = f'{np.random.rand()}'
        reading = float(inst.query(':MEASure:FProbe:Efield:MAG?'))
        out = f'{reading:0.4f}'

        print(out)
        ser.write(b'\x13\x11  '+out.encode()+b'\r\n')

    if sample.decode().startswith('FREQuency'):
        freq = sample.decode().split(' ')[1]
        freq = float(freq)
        print(f'freq {freq/1e6}')
        inst.write(f':SYSTem:FREQuency {freq}')

        
ser.close()
