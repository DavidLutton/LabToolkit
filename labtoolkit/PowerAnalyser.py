#!/usr/bin/env python3
"""."""
# import time
# import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np
from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class PowerAnalyser(GenericInstrument):
    """Parent class for PowerAnalysers."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return"{}, {}".format(__class__, self.instrument)


class VoltechPM3000A(PowerAnalyser, IEEE488):
    """Voltech PM3000A.

    .. figure::  images/PowerAnalyser/VoltechPM3000A.jpg
    """


class VoltechPM1000P(PowerAnalyser, IEEE488):
    """Voltech PM1000+.

    .. figure::  images/PowerAnalyser/VoltechPM1000P.jpg
    """


REGISTER = {
    'VoltechPM3000A': VoltechPM3000A,
    'VoltechPM1000P': VoltechPM1000P,
    # Benchview suppported  PA2201A, PA2203A

}
