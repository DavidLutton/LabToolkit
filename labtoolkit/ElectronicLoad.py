#!/usr/bin/env python3
"""."""
# import time
# import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np
from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class ElectronicLoad(GenericInstrument):
    """Parent class for ElectronicLoad."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return"{}, {}".format(__class__, self.instrument)


class RigolDL30n1(ElectronicLoad, IEEE488):
    """Rigol DL30n1 Family.

    .. figure::  images/ElectronicLoad/RigolDL3021.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

    def __repr__(self):
        """."""
        return "{}, {}".format(__class__, self.instrument)

    @property
    def voltagedc(self):
        """."""
        return float(self.query(':MEASure:VOLTage:DC?'))

    # @validsteps(3,4,5,6)
    @voltagedc.setter
    def voltagedc(self, voltage):
        self.write(':SOURce:VOLTage:LEVel:IMMediate {0:.3f}'.format(voltage))

    @property
    def currentdc(self):
        """."""
        return float(self.query(':MEASure:CURRent:DC?'))

    @currentdc.setter
    def currentdc(self, current):
        self.write(':SOURce:CURRent:LEVel:IMMediate {0:.3f}'.format(current))

    @property
    def function(self):
        """."""
        self.query(':SOURce:FUNCtion?')

    @function.setter
    def function(self, function):
        self.write(':SOURce:FUNCtion {}'.format(function))

    # :[SOURce]:TRANsient bool


REGISTER = {
    'RIGOL,DL3031A': RigolDL30n1,
    # Benchview supported  N3300A, N3301A, 6060B, 6063B

}
