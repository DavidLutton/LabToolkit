#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class Positioner(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


REGISTER = {
    "ZZZ": Positioner,

}
