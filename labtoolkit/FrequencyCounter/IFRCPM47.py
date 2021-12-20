import serial
from serial.tools import list_ports

from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class IFR_CPM():
    
    def __init__(self, inst):
        self.inst = serial.Serial(inst, 9600, timeout=1, bytesize=8, parity='N', stopbits=1)

    def query(self, command):
        self.inst.write(command)
        # ser.write(command.encode('ascii') + b'\r')
        return self.inst.readline()  # .strip()

    def counter(self):
        multipliers = {' Hz': 1, 'kHz': 1e3, 'MHz': 1e6, 'GHz': 1e9 }

        while self.inst.isOpen():
            self.inst.write(b'\r')
            if self.inst.read(7).strip() == b'>>':  # wait for prompt characters
                if self.query(b'DISPLAY FREQ\r') == b'DISPLAY FREQ\r\n':  # request frequency data
                    # The next readline should be frequency
                    ret = self.inst.readline().decode()  # 50.015 623 MHz 0 0 0 0 0

                    ret = ret[:-12].strip()  # 50.015 623 MHz
                    magnitude, multiplier = float(ret[:-3].replace(' ', '')), ret[-3:]  # 50.015623, 'MHz'

                    # print(f'magnitude {magnitude}, multiplier {multiplier}')
                    value = int(magnitude * multipliers[multiplier])

                    # print(f'{value} Hz')
                    yield value

