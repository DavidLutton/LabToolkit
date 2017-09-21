"""."""
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from engineering_project.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class FieldStrength(GenericInstrument):
    """."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))


class EMR20(FieldStrength):
    """Wandel and Goltermann EMR-20 Field Strength probe.

    .. figure::  images/FieldStrength/EMR20.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
            inst.write(init)

        inst.read()  # read the init feedback
        # b'\x13\x11\x13\x11\x13\x11\x13\x11\x13\x11'

    def readback(self):
        """Readback Field Strength."""
        # pass
        sample = inst.query('M')
        return float((sample.split(b'\x13\x11')[1]).decode().strip())
        # sample = ser.readline()
        # sample = b'\x13\x11    0.80\r\n'  # a example of a readline

        # return float((sample.split(b'\x13\x11')[1]).decode().strip())
        # remove control codes / line encodes and return a float value


class Narda601(FieldStrength):
    """Narda601.

    .. figure::  images/FieldStrength/Narda601.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

    def setup(self):
        """Send setup commands to probe."""
        pass

    def readback(self):
        """Readback Field Strength."""
        pass


class EMCO7110(FieldStrength):
    """."""


class EMC20(FieldStrength):
    """."""


REGISTER = {
    'EMR20': EMR20,
    'Narda601': Narda601,
    'EMCO7110': EMCO7110,
    'EMC20': EMC20,
}
