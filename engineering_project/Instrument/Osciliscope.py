#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from Instrument.GenericInstrument import GenericInstrument as GenericInstrument


class Oscilloscope(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


# class TektronixTDS544A(Oscilloscope):  # 500e6 1GS/s

class AgilentDSO5052A(Oscilloscope):  # 500e6 4GS/s

    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # assert self.IDN.startswith('Agilent Technologies, DSO5052A,')


register = {
    "ZZZ": AgilentDSO5052A,

}
