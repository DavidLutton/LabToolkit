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

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    @property
    def attenuation(self):
        return(float(self.query("ATTN?")))

    @attenuation.setter
    def attenuation(self, frequency):
        self.write("ATTN  {0:.1f}DB".format(attenuation))
