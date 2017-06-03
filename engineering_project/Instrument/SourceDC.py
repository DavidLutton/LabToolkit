#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


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
        self.write("V1{}".format(volts))

    @property
    def current(self):
        """."""
        self.query('I1?')

    @current.setter
    def current(self, current):
        self.write("I1{}".format(current))

    @property
    def output(self):
        """."""
        self.query('OP1?')

    @output.setter
    def output(self, boolean=False):
        self.write("OP1 {:d}".format(boolean))


REGISTER = {
    "ZZZ": SourceDC,
    'THURLBY-THANDAR,PL330P,0,1.10': TTIPL330P,

}
