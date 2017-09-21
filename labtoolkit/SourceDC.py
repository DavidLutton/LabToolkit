#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from labtoolkit.GenericInstrument import GenericInstrument
    from labtoolkit.IEEE488 import IEEE488
    from labtoolkit.SCPI import SCPI

except ImportError:
    from GenericInstrument import GenericInstrument
    from IEEE488 import IEEE488
    from SCPI import SCPI


class SourceDC(GenericInstrument):
    """DC power sources."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    @property
    def volts(self):
        """Not Implemented Stub."""
        return NotImplemented

    @volts.setter
    def volts(self, volts):
        return NotImplemented

    @property
    def current(self):
        """Not Implemented Stub."""
        return NotImplemented

    @current.setter
    def current(self, current):
        return NotImplemented

    @property
    def output(self):
        """Not Implemented Stub."""
        return NotImplemented

    @output.setter
    def output(self, boolean=False):
        return NotImplemented


class HP6632A(SourceDC):
    """HP 6632A 0-20V/0-5A,100W.

    .. figure::  images/SourceDC/HP6632A.jpg
    """

    @property
    def volts(self):
        """."""
        return NotImplemented


class TTIPL303(SourceDC):
    """."""

    @property
    def volts(self):
        """."""
        return float(self.query('V1?'))

    @property
    def voltsoutput(self):
        """."""
        return float(self.query('V{}O?'.format(1)))

    @volts.setter
    def volts(self, volts):
        self.write('V1{2.3f}'.format(volts))

    @property
    def current(self):
        """."""
        return float(self.query('I1?'))

    @property
    def currentoutput(self):
        """."""
        return float(self.query('I{}O?'.format(1)))

    @current.setter
    def current(self, current):
        self.write('I1{1.3f}'.format(current))

    @property
    def output(self):
        """."""
        return bool(self.query('OP1?'))

    @output.setter
    def output(self, boolean=False):
        self.write('OP1 {:d}'.format(boolean))

    @property
    def config(self):
        """."""
        return self.query('CONFIG?')

    @property
    def currentrange(self):
        """."""
        return int(self.query('IRANGE{}?'.format(1)))

    @currentrange.setter
    def currentrange(self, currentrange):
        self.write('IRANGE{}{}'.format(1, currentrange))

    @property
    def voltsoverprotect(self):
        """."""
        return(float(self.query('OVP{}?'.format(1))))

    @property
    def currentoverprotect(self):
        """."""
        return(float(self.query('OCP{}?'.format(1))))

    # def setLocal(self): 'LOCAL'


class TTIPL330P(SourceDC):
    """TTI PL330P 0-32V/0-3A.

    IDN: THURLBY-THANDAR,PL330P,0,1.10

    .. figure::  images/SourceDC/TTIPL330P.jpg
    """

    '''
-> *IDN?
<- THURLBY-THANDAR,PL330P,0,1.10

-> V1?
<- V1 0.00

-> I1?
<- I1 0.001

-> *LRN?
<- I1 0.001;V1 0.00;OP1 0;DELTAV1 0.01;DELTAI1 0.001;DAMPING1 1

-> V1 5
-> V1?
<- V1 5.00


-> I1 5

-> I1?
<- I1 1.000

-> *LRN?
<- I1 0.001;V1 0.00;OP1 0;DELTAV1 0.01;DELTAI1 0.001;DAMPING1 1

-> OP1 1
  Output on
-> OP1 0
  Output off


http://forums.ni.com/ni/attachments/ni/170/181751/1/PL-P%20Instruction%20Manual.pdf


http://www.tti-test.com/downloads/drivers-download.htm
    '''

    @property
    def volts(self):
        """."""
        self.query('V1?')

    @volts.setter
    def volts(self, volts):
        self.write('V1{}'.format(volts))

    @property
    def current(self):
        """."""
        self.query('I1?')

    @current.setter
    def current(self, current):
        self.write('I1{}'.format(current))

    @property
    def output(self):
        """."""
        self.query('OP1?')

    @output.setter
    def output(self, boolean=False):
        self.write('OP1 {:d}'.format(boolean))


REGISTER = {
    'HEWLETT-PACKARD,6632A,': HP6632A,
    'THURLBY-THANDAR,PL330P,': TTIPL330P,
    'THURLBY THANDAR,PL303,': TTIPL303,  # ? *IDN?
    # 'THURLBY THANDAR,MX100TP,': TTIMX100TP,
    # 'THURLBY THANDAR,MX180TP,': TTIMX180TP,
    # TTI, CPX400DP
    # 'Rohde & Schwarz, HMC8043,':
    # 'Rohde & Schwarz, HMC8042,':
    # 'Rohde & Schwarz, HMC8041,':
    # Keithley, 2231A-30-3
    # Keithley, 2220-30-1
    # BKPrecision, BK9130B
    # BKPrecision, BK9181B
    # Keysight, E3648A
    # Keysight, E3634A
    # Keysight, E3649A
    # Keysight, E3631A
    # Keysight, E3644A
    # Keysight, E36104A
    # GWINSTEK, GPD-4303S
    # GWINSTEK, GPD-2303S
    # Keithley, 2220-30-1



}
