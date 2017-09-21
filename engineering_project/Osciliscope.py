#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from engineering_project.GenericInstrument import GenericInstrument
    from engineering_project.IEEE488 import IEEE488
    from engineering_project.SCPI import SCPI

except ImportError:
    from GenericInstrument import GenericInstrument
    from IEEE488 import IEEE488
    from SCPI import SCPI


class Oscilloscope(GenericInstrument):
    """Parent class for Oscilloscope."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def trace(self):
        """."""
        return NotImplemented


class TektronixTDS544A(Oscilloscope):
    """Tektronix TDS544A 500e6 1GS/s.

    .. figure::  images/Oscilloscope/TektronixTDS544A.jpg
    """

    def trace(self):
        """."""
        return NotImplemented


class AgilentDSO5052A(Oscilloscope):
    """Agilent DSO5052A 500e6 4GS/s.

    .. figure::  images/Oscilloscope/AgilentDSO5052A.jpg
    """

    def trace(self):
        """."""
        return NotImplemented


class KeysightDSOX3034T(Oscilloscope):
    """KeysightDSOX3034T 350e6 5GS/s.

    .. figure::  images/Oscilloscope/KeysightDSOX3034T.jpg
    """

    def trace(self):
        """."""
        return NotImplemented


class AttenInstrumentsADS1102CAL(Oscilloscope):
    """Atten Instruments ADS1102CAL 100e6 1GS/s.

    .. figure::  images/Oscilloscope/AttenInstrumentsADS1102CAL.jpg
    """

    def trace(self):
        """."""
        return NotImplemented

    '''def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # assert self.IDN.startswith('Agilent Technologies, DSO5052A,')
'''


REGISTER = {
    'AGILENT TECHNOLOGIES,DSO5052A': AgilentDSO5052A,
    'Tektronix,TDS 544A': TektronixTDS544A,
    'Keysight,DSOX3034T': KeysightDSOX3034T,
    'AttenInstruments,ADS1102CAL': AttenInstrumentsADS1102CAL,
}
