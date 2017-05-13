#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class Oscilloscope(GenericInstrument):
    """Parent class for Oscilloscope."""

    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


class TektronixTDS544A(Oscilloscope):
    """Tektronix TDS544A 500e6 1GS/s.

    .. figure::  images/Oscilloscope/TektronixTDS544A.jpg
    """



class AgilentDSO5052A(Oscilloscope):
    """Agilent DSO5052A 500e6 4GS/s.

    .. figure::  images/Oscilloscope/AgilentDSO5052A.jpg
    """


    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # assert self.IDN.startswith('Agilent Technologies, DSO5052A,')


REGISTER = {
    "ZZZ": AgilentDSO5052A,


}
