#!/usr/bin/env python3
"""."""
import time
import logging
# import pint

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class FrequencyCounter(GenericInstrument):
    """Parent class for FrequencyCounter."""

    def __init__(self, instrument):
        super().__init__(instrument)

    def frequency_error(self, target=10e6):
        return round(self.frequency - target, 8)


class MarconiCPM47(FrequencyCounter):
    """40GHz counter 1Hz step.

    .. figure::  images/FrequencyCounter/CPM47.jpg
    """

    def __repr__(self):
        return(f"{__class__}, {self.instrument}")

    def __init__(self, inst):
        self.inst = serial.Serial(inst, 9600, timeout=1, bytesize=8, parity='N', stopbits=1)

    def query(self, command):
        self.inst.write(command)
        # ser.write(command.encode('ascii') + b'\r')
        return self.inst.readline()  # .strip()

    def counter(self):
        multipliers = {' Hz': 1, 'kHz': 1e3, 'MHz': 1e6, 'GHz': 1e9}

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


class HP_53132A(Counter):

    def __init__(self, inst):
        self.inst = inst
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        '''
        *IDN?
        HEWLETT-PACKARD,53132A,0,4806

        :SENSe:ROSCillator:SOURce?
        EXT


        :SENSe:ROSCillator:SOURce:AUTO?
        1/0

        :SENSe:ROSCillator:SOURce:AUTO OFF

        :READ?
        Single read of float value, trigger becomes single

        :FETCh?
        Fetch of current of float value, trigger remains continuous


        >>> round(10000000.000583 - 10e6, 8)
        '''

    @property
    def frequency(self):
        return float(self.inst.query('FETCH:FREQUENCY?'))


REGISTER = {
    # 'MarconiCPM47': MarconiCPM47,
    'HP_53132A': HP_53132A,  # TODO
    # 'T4000': HP3457A,
    # Benchview supported 53210A, 53220A, 53230A
}
