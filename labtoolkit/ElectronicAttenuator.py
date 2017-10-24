#!/usr/bin/env python3
"""."""
# import time
# import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class ElectronicAttenuator(GenericInstrument):
    """Parent class for ElectronicAttenuators."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return"{}, {}".format(__class__, self.instrument)


class MarconiInstruments2187(ElectronicAttenuator, IEEE488):
    """Marconi 2187 - DC-20GHz 1W max N-type.

    .. figure::  images/ElectronicAttenuator/MarconiInstruments2187.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

    def __repr__(self):
        """."""
        return "{}, {}".format(__class__.__name__, self.instrument)

    @property
    def attenuation(self):
        """Attenuation of labtoolkit."""
        return float(self.query("ATTN?"))

    # @validsteps(3,4,5,6)
    @attenuation.setter
    def attenuation(self, attenuation):
        self.write("ATTN {0:.0f}DB".format(attenuation))

    def preset(self):
        """."""
        self.attenuation = 144


REGISTER = {
    "MARCONI INSTRUMENTS,2187,": MarconiInstruments2187,

}
