#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from Instrument.GenericInstrument import GenericInstrument as GenericInstrument


class FieldStrength(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


register = {
    "ZZZ": FieldStrength,
    # EMC-20 # setup & readback DONE
    # SI-100
    # EMCO 7110


}
