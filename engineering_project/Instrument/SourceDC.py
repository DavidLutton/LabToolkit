#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class SourceDC(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


class HP6632A(SourceDC):
    """HP 6632A 0-20V/0-5A,100W.

    .. figure::  images/SourceDC/HP6632A.jpg
    """


REGISTER = {
    "ZZZ": SourceDC,

}
