#!/usr/bin/env python3
"""."""

import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class Oscilloscope(GenericInstrument):
    """Parent class for Oscilloscope."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def trace(self):
        """."""
        return NotImplemented


class TektronixTDS544A(Oscilloscope):
    """Tektronix TDS544A 500e6 1GS/s.

    .. figure::  images/Oscilloscope/TektronixTDS544A.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def trace(self):
        """."""
        return NotImplemented


class AgilentDSO5052A(Oscilloscope):
    """Agilent DSO5052A 500e6 4GS/s.

    .. figure::  images/Oscilloscope/AgilentDSO5052A.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def trace(self):
        """."""
        return NotImplemented


class KeysightDSOX3034T(Oscilloscope):
    """KeysightDSOX3034T 350e6 5GS/s.

    .. figure::  images/Oscilloscope/KeysightDSOX3034T.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def trace(self):
        """."""
        return NotImplemented


class AttenInstrumentsADS1102CAL(Oscilloscope):
    """Atten Instruments ADS1102CAL 100e6 1GS/s.

    .. figure::  images/Oscilloscope/AttenInstrumentsADS1102CAL.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def trace(self):
        """."""
        return NotImplemented

    '''def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # assert self.IDN.startswith('Agilent Technologies, DSO5052A,')
'''


REGISTER = {
    'AGILENT TECHNOLOGIES,DSO5052A': AgilentDSO5052A,
    'Tektronix,TDS 544A': TektronixTDS544A,
    'KEYSIGHT TECHNOLOGIES,DSO-X 3034T': KeysightDSOX3034T,
    'AttenInstruments,ADS1102CAL': AttenInstrumentsADS1102CAL,
    # Benchview supported DSO6054L, DSO6104L, DSO6104L, DSO5014A, DSO5032A, DSO5034A, DSO5052A, DSO5054A, DSO6012A, DSO6014A, DSO6014L, DSO6032A, DSO6034A, DSO6052A, DSO6054A, DSO6054L, DSO6102A,
    #                     DSO6104A, DSO6104L, DSO7012A, DSO7012B, DSO7014A, DSO7014B, DSO7032A, DSO7032B, DSO7034A, DSO7034B, DSO7052A, DSO7052B, DSO7054A, DSO7054B, DSO7104A, DSO7104B, DSO90254A,
    #                     DSO90404A, DSO90604A, DSO9064A, DSO90804A, DSO9104A, DSO91204A, DSO91304A, DSO9254A, DSO9404A, DSOS054A, DSOS104A, DSOS204A, DSOS254A, DSOS404A, DSOS604A, DSOS804A,
    # Benchview supported DSO-X 2002A, DSO-X 2004A, DSO-X 2012A, DSO-X 2014A, DSO-X 2022A, DSO-X 2024A, DSO-X 3012A, DSO-X 3012T, DSO-X 3014A, DSO-X 3014T, DSO-X 3022T, DSO-X 3024A, DSO-X 3024T,
    #                     DSO-X 3032A, DSO-X 3032T, DSO-X 3034A, DSO-X 3034T, DSO-X 3052A, DSO-X 3052T, DSO-X 3054A, DSO-X 3054T, DSO-X 3102A, DSO-X 3102T, DSO-X 3104A, DSO-X 3104T, DSO-X 4022A,
    #                     DSO-X 4024A, DSO-X 4032A, DSO-X 4034A, DSO-X 4052A, DSO-X 4054A, DSO-X 4104A, DSO-X 4154A,
    # Benchview supported DSOX1102A, DSOX1102G, DSOX6002A , DSOX6004A , DSOX91304A, DSOX91604A, DSOX92004A, DSOX92004Q, DSOX92504A, DSOX92504Q, DSOX92804A, DSOX93204A,
    #                     DSOX93304Q, DSOX95004Q, DSOX96204Q
    # Benchview supported EDUX1002A, EDUX1002G,
    # Benchview supported MSO6012A, MSO6014A, MSO6032A, MSO6034A, MSO6052A, MSO6054A, MSO6102A, MSO6104A, MSO7012A, MSO7012B, MSO7014A, MSO7014B, MSO7032A, MSO7032B, MSO7034A, MSO7034B, MSO7052A,
    #                     MSO7052B, MSO7054A, MSO7054B, MSO7104A, MSO7104B, MSO9064A, MSO9104A, MSO9254A, MSO9404A, MSOS054A, MSOS104A, MSOS204A, MSOS254A, MSOS404A, MSOS604A, MSOS804A,
    # Benchview supported MSO-X 2002A, MSO-X 2004A, MSO-X 2012A, MSO-X 2014A, MSO-X 2022A, MSO-X 2024A, MSO-X 3012A, MSO-X 3012T, MSO-X 3014A, MSO-X 3014T, MSO-X 3022T,
    #                     MSO-X 3024A, MSO-X 3024T, MSO-X 3032A, MSO-X 3032T, MSO-X 3034A, MSO-X 3034T, MSO-X 3052A, MSO-X 3052T, MSO-X 3054A, MSO-X 3054T, MSO-X 3102A, MSO-X 3102T, MSO-X 3104A,
    #                     MSO-X 3104T, MSO-X 4022A, MSO-X 4024A, MSO-X 4032A, MSO-X 4034A, MSO-X 4052A, MSO-X 4054A, MSO-X 4104A, MSO-X 4154A,
    # Benchview supported MSOX6002A , MSOX6004A , MSOX91304A, MSOX91604A, MSOX92004A, MSOX92504A, MSOX92804A, MSOX93204A
}
