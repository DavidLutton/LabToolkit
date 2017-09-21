#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from labtoolkit.GenericInstrument import GenericInstrument
    from labtoolkit.IEEE488 import IEEE488
    from labtoolkit.SCPI import SCPI

except ImportError:
    from GenericInstrument import GenericInstrument
    from IEEE488 import IEEE488
    from SCPI import SCPI


class Positioner(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


REGISTER = {
    "ZZZ": Positioner,

}
