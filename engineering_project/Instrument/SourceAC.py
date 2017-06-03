#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class SourceAC(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    @property
    def volts(self):
        """Not Implemented Stub."""
        return NotImplemented

    @volts.setter
    def volts(self, volts):
        return NotImplemented

    @property
    def frequency(self):
        """Not Implemented Stub."""
        return NotImplemented

    @frequency.setter
    def frequency(self, current):
        return NotImplemented

    @property
    def output(self):
        """Not Implemented Stub."""
        return NotImplemented

    @output.setter
    def output(self, boolean=False):
        return NotImplemented

    @property
    def current(self):
        """Not Implemented Stub."""
        return NotImplemented

    @current.setter
    def current(self, current):
        return NotImplemented


class CaliforniaInstruments3000i(SourceAC):
    """California Instruments 3000i.

    .. figure::  images/SourceAC/CaliforniaInstruments3000i.jpg
    """


class CaliforniaInstruments3000iM(SourceAC):
    """California Instruments 3000i.

    .. figure::  images/SourceAC/CaliforniaInstruments3000iM.jpg
    """


REGISTER = {
    "ZZZ": SourceAC,

}
