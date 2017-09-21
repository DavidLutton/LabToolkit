#!/usr/bin/env python3
import time
import logging
import pint

try:
    from labtoolkit.GenericInstrument import GenericInstrument
    from labtoolkit.IEEE488 import IEEE488
    from labtoolkit.SCPI import SCPI

except ImportError:
    from GenericInstrument import GenericInstrument
    from IEEE488 import IEEE488
    from SCPI import SCPI


class SurgeGenerator(GenericInstrument):
    """Parent class for SurgeGenerator."""

    def __init__(self, instrument):
        super().__init__(instrument)


class T2000(SurgeGenerator):
    """T2000.

    .. figure::  images/SurgeGenerator/T2000.jpg
    """

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))


REGISTER = {
    'T2000': T2000,
    # 'T4000': HP3457A,
}
