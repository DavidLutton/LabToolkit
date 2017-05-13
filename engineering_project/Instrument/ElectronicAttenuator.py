#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np
try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class ElectronicAttenuator(GenericInstrument):
    """Parent class for ElectronicAttenuators."""

    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


class Marconi2187(ElectronicAttenuator):
    """Marconi 2187 - DC-20GHz 1W max N-type.

    .. figure::  images/ElectronicAttenuator/Marconi2187.jpg
    """

    def __init__(self, instrument, logger=None):
        self.dBm = "DB"
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith("MARCONI INSTRUMENTS,2187,")

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    @property
    def attenuation(self):
        """Attenuation of instrument."""
        return(float(self.query("ATTN?")))

    @attenuation.setter
    def attenuation(self, attenuation):
        self.write("ATTN {0:.1f}{}".format(attenuation, self.dBm))


REGISTER = {
    "MARCONI INSTRUMENTS,2187,": Marconi2187,

}
