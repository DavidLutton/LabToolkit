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


class EnviromentalChamber(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


class ZZZ(EnviromentalChamber):
    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith("ZZZ")

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    @property
    def temperature(self):
        return(float(self.query("THERM?")))

    @temperature.setter
    def temperature(self, temperature):
        self.write("THERM {0:.0f}".format(temperature))


REGISTER = {
    'ZZZ': ZZZ,
}
