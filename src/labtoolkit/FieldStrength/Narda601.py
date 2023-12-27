import binascii
import math
import struct

from pprint import pprint

# import serial
# from serial.tools import list_ports

from ..Instrument import Instrument


class Narda601(Instrument):
    """Narda601.

    .. figure::  images/FieldStrength/Narda601.jpg
    """

    def setup(self):
        """Send setup commands to probe."""
        pass

    def readback(self):
        """Readback Field Strength."""
        pass


    def binarytoVm(self, binary=b'T\x00\x00\x00\x00'):
        if binary[0] == 84:  # ASCII capital T, 54 as hex, 84 as decimal
            binary = binary[1:]  # Remove leading character from binary 'T'
            value = struct.unpack('<f', binary)[0]  # unpack from binary
            # print('Value: {}\t::\tBinary: {}'.format(math.sqrt(value), binary))  # print(Hex, Value, Binary)
            return math.sqrt(value)  # Square root of value
        else:
            return ValueError  # if data was not ‘T’ Total Field, return ValueError


    def returnstr(self, binary=b'T\x00\x00\x00\x00'):
        return binary[1:].decode()  # Remove leading character from binary and decode


    def decode_example(self, hexes):
        for hexstring in hexes:
            hexstring = hexstring.replace(' ', '')  # Remove spaces in hexstring
            bins = binascii.unhexlify(hexstring)  # encode to binary, as you would receive over serial
            print('{}\t::\t{}\t::\t{}'.format(hexstring, self.binarytoVm(bins), bins))  # print(Hex, Value, Binary)


    def query(self, ser, command):
        ser.write(command.encode('ascii') + b'\r\n')
        return ser.readline()

'''

hexes = [
    '54 00 00 00 00',
    '54 30 45 B5 3E',
    '54 DD C3 B9 3F',
    '54 62 81 10 40',
    '54 7F 0A 52 40',
    '54 76 82 FB 40',
    '54 63 FE 0A 41',
    '54 2E EC D1 40',
    '54 30 43 B5 3E',
    '54 00 C7 B9 3F',
    '54 02 47 D8 3E',
    '54 02 91 B5 3F',
    '54 08 10 3C 3F',
    '54 11 22 2A 40',
    '54 16 4B 61 40',
    '54 19 EA 20 41',
    '54 26 5C 34 40',
    '54 27 9B D8 3E',
    '54 28 7E ED 40',
    '54 2E EC D1 40',
    '54 30 43 B5 3E',
    '54 30 43 B5 3E',
    '54 4E 97 D0 3F',
    '54 52 85 11 3F',
    '54 52 85 11 3F',
    '54 53 EE EF 3F',
    '54 62 81 10 40',
    '54 63 FE 0A 41',
    '54 6A 01 E7 3F',
    '54 6C 8B 74 3F',
    '54 70 4F DD 3F',
    '54 76 82 FB 40',
    '54 77 13 29 40',
    '54 77 13 29 40',
    '54 78 CD 40 40',
    '54 78 CD 40 40',
    '54 7B 1F 52 3F',
    '54 7B 1F 52 3F',
    '54 7F 0A 52 40',
    '54 83 58 AE 3E',
    '54 83 58 AE 3E',
    '54 8C DC E5 40',
    '54 9E 4F 01 40',
    '54 9F 14 C7 3F',
    '54 A4 82 95 3F',
    '54 A7 D6 04 40',
    '54 A9 33 72 40',
    '54 AF B3 02 3F',
    '54 B4 BA 27 40',
    '54 BE E3 39 40',
    '54 C2 4F 43 3F',
    '54 C8 89 02 40',
    '54 D0 47 08 3D',
    '54 D3 C5 08 40',
    '54 DE A5 94 3F',
    '54 F5 B7 04 3F',
]



menu = {}
menu[1] = ['Read total field', '#00?T*', binarytoVm]
menu[2] = ['Read serial number', '#00?s*', returnstr]
menu[3] = ['Read version number', '#00?v*', returnstr]
menu[4] = ['Read part? number', '#00?p*', returnstr]

# menu[5] = ['Read battery voltage - no decoder', '#00?b*', returnstr]
menu[9] = ['Decode example hex values', None, decode_example]



# pprint(menu)
for each in list_ports.comports():
    print('{}\t\t{}'.format(each.device, each.description))
port = input('Serial Port? : ')

with serial.Serial(port, 9600, timeout=1, bytesize=8, parity='N', stopbits=1) as ser:
    while ser.isOpen():
        print()
        for entry in sorted(menu):
            print('{}: {}'.format(str(entry), menu[entry][0]))
        try:
            selection = int(input('\nSelection: '))
        except ValueError as e:
            selection = -1
        finally:
            try:
                if menu[selection][1] is not None:
                    print(menu[selection][2](query(ser, menu[selection][1])))
                else:
                    menu[selection][2]()
            except KeyError as e:
                print('Unknown selection: {}'.format(e))
            
'''
