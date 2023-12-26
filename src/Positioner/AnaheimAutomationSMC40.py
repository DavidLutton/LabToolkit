from ..Instrument import Instrument
from time import sleep


class AnaheimAutomationSMC40(Instrument):

    # http://www.anaheimautomation.com/manuals/stepper/L010098%20-%20SMC40%20Users%20Guide.pdf

    @property
    def heading(self):
        return NotImplemented

    @heading.setter
    def heading(self, clockwise=True):
        if clockwise is True:
            self.write('D+')  # Clockwise
        else:
            self.write('D-')  # Anti-Clockwise

    @property
    def stepangle(self):
        return NotImplemented

    @stepangle.setter
    def stepangle(self, stepangle=1):  # 100 is 1 degree
        self.write(f'XMN{int(stepangle * 100)}')
        # int(Q_(stepangle, 'degree').magnitude * 100)
        # self.write('XMN{}'.format(int(Q_(stepangle, 'degree').magnitude * 100)))

    def zero(self):
        self.write('XGH')

    def init(self):
        self.write('@0')

    def IDN(self):
        return self.query('ID')

    def WAI(self):
        return self.query('XMC')  # ??

    def TRG(self):
        self.write('XGR')

    def move(self, clockwise=True, angle=1, wait=True):
        self.stepsize = angle
        self.heading = clockwise
        self.write('XGR')
        if wait is True:
            self.WAI()

'''
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
        
'''