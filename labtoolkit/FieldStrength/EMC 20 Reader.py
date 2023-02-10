import sys
import serial


def read(ser):
    """Remove control codes / line encodes and return a float value."""
    ser.write('M\r\n'.encode())  # Ask for a value

    sample = ser.readline()
    # print(sample)
    # sample = b'\x13\x11    0.80\r\n'  # a example of a readline
    if sample != b'':
        return float((sample.split(b'\x13\x11')[1]).decode().strip())
    else:
        return None
    

for port in serial.tools.list_ports.comports():
    print(f'{port.name}  == {port.description}')
port = input('Serial COM port? : ')
ser = serial.Serial(port, 4800, timeout=2)

for init in [
        'CALC:CAL 1.00\r\n',
        'CALC:UNIT E_FIELD\r\n',
        'SYST:KLOC ON\r\n',
        'FAST:MODE ON\r\n',
        'CALC:AXIS EFF\r\n'
    ]:
    print(init)
    ser.write(init.encode())
    
ser.readline() # read the init feedback
# b'\x13\x11\x13\x11\x13\x11\x13\x11\x13\x11'

while [ True ]:
    sample = read(ser)
    print(sample)

ser.close()
