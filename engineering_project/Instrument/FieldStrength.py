#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class FieldStrength(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


class EMR20(FieldStrength):
    """Wandel and Goltermann EMR-20 Field Strength probe.

    .. figure::  images/FieldStrength/EMR20.jpg"""

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

    def setup(self):
        """Send setup commands to probe."""
        pass

    def readback(self):
        """Readback Field Strength."""
        pass


REGISTER = {
    "ZZZ": FieldStrength,
    # EMC-20 # setup & readback DONE
    # SI-100
    # EMCO 7110


}
