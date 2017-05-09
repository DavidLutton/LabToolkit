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


class CaliforniaInstruments3000i(SourceAC):
    """California Instruments 3000i.

    .. figure::  images/SourceAC/CaliforniaInstruments3000i.jpg
    """


class CaliforniaInstruments3000iM(SourceAC):
    """California Instruments 3000i.

    .. figure::  images/SourceAC/CaliforniaInstruments3000iM.jpg
    """


register = {
    "ZZZ": SourceAC,

}
