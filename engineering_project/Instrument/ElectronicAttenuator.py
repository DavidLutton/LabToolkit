#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from Instrument.GenericInstrument import GenericInstrument as GenericInstrument


class ElectronicAttenuator(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


class Marconi2187(ElectronicAttenuator):
    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith("MARCONI INSTRUMENTS,2187,")
        self.attenuation = float(self.query("ATTN?"))

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def set(self, attenuation):
        if attenuation != self.attenuation:
            self.write("ATTN  {0:.1f}DB".format(attenuation))
            self.attenuation = attenuation
