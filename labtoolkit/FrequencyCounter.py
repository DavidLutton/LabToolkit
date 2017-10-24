#!/usr/bin/env python3
"""."""
import time
import logging
# import pint

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class FrequencyCounter(GenericInstrument):
    """Parent class for FrequencyCounter."""

    def __init__(self, instrument):
        super().__init__(instrument)


class MarconiCPM47(FrequencyCounter):
    """40GHz counter 1Hz step.

    .. figure::  images/FrequencyCounter/CPM47.jpg
    """

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

    @property
    def frequency(self):
        """."""
        return float(self.query("FREQuency?"))


REGISTER = {
    'MarconiCPM47': MarconiCPM47,
    # 'T4000': HP3457A,
    # Benchview supported 53210A, 53220A, 53230A
}
