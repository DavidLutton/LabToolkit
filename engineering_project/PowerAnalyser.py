# import time
# import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np
try:
    from engineering_project.GenericInstrument import GenericInstrument
    from engineering_project.IEEE488 import IEEE488
    from engineering_project.SCPI import SCPI

except ImportError:
    from GenericInstrument import GenericInstrument
    from IEEE488 import IEEE488
    from SCPI import SCPI


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

}
