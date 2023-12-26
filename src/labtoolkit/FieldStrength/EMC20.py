
import sys
import serial


class EMC20():
    """Wandel and Goltermann EMR-20 Field Strength probe.

    .. figure::  images/FieldStrength/EMR20.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # ser = serial.Serial('COM5', 4800, timeout=2)

    def setup(self):
        """Send setup commands to probe."""
        for init in [
                'CALC:CAL 1.00\r\n',
                'CALC:UNIT E_FIELD\r\n',
                'SYST:KLOC ON\r\n',
                'FAST:MODE ON\r\n',
                'CALC:AXIS EFF\r\n'
        ]:
            # print(init.strip())
            self.write(init)

        self.read()  # read the init feedback
        # b'\x13\x11\x13\x11\x13\x11\x13\x11\x13\x11'

    def readback(self):
        """Readback Field Strength."""
        sample = self.query('M')
        return float((sample.split(b'\x13\x11')[1]).decode().strip())
        # sample = ser.readline()
        # sample = b'\x13\x11    0.80\r\n'  # a example of a readline

        # return float((sample.split(b'\x13\x11')[1]).decode().strip())
        # remove control codes / line encodes and return a float value

    def read(self):
        """Remove control codes / line encodes and return a float value."""
        self.write('M\r\n'.encode())  # Ask for a value

        sample = self.readline()
        # print(sample)
        # sample = b'\x13\x11    0.80\r\n'  # a example of a readline
        if sample != b'':
            return float((sample.split(b'\x13\x11')[1]).decode().strip())
        else:
            return None
