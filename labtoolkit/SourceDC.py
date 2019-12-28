#!/usr/bin/env python3
"""."""

import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class SourceDC(GenericInstrument):
    """DC power sources."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

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
        return float(self.query(f'V{1}O?'))

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
        return float(self.query(f'I{1}O?'))

    @current.setter
    def current(self, current):
        self.write('I1{1.3f}'.format(current))

    @property
    def output(self):
        """."""
        return bool(self.query('OP1?'))

    @output.setter
    def output(self, boolean=False):
        self.write(f'OP1 {boolean:d}')

    @property
    def config(self):
        """."""
        return self.query('CONFIG?')

    @property
    def currentrange(self):
        """."""
        return int(self.query(f'IRANGE{1}?'))

    @currentrange.setter
    def currentrange(self, currentrange):
        self.write(f'IRANGE{1}{currentrange}')

    @property
    def voltsoverprotect(self):
        """."""
        return(float(self.query(f'OVP{1}?')))

    @property
    def currentoverprotect(self):
        """."""
        return(float(self.query(f'OCP{1}?')))

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
        self.write(f'V1{volts}')

    @property
    def current(self):
        """."""
        self.query('I1?')

    @current.setter
    def current(self, current):
        self.write(f'I1{current}')

    @property
    def output(self):
        """."""
        self.query('OP1?')

    @output.setter
    def output(self, boolean=False):
        self.write(f'OP1 {boolean:d}')


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
    # Benchview supported E3631A, E3632A, E3633A, E3634A, E3640A, E3641A, E3642A, E3643A, E3644A, E3645A, E3646A, E3647A, E3648A, E3649A, E36102A, E36103A, E36104A, E36105A, E36106A, E36310A,
    # Benchview supported E36311A, E36312A, E36313A, N6700A/B/C,
    # Benchview supported N6701A/C, N6702A/C, N6705A/B/C, N6950A, N6951A, N6952A, N6953A, N6954A, N6970A, N6971A, N6972A, N6973A, N6974A, N6976A, N6977A, N7950A, N7951A, N7952A, N7953A, N7954A,
    # Benchview supported N7970A, N7971A, N7972A, N7973A, N7974A, N7976A, N7977A, N6785A, N6786A, B2901A, B2902A,
    # Benchview supported B2911A,B2912A, B2961A, B2962A, N5741A, N5742A, N5743A, N5744A, N5745A, N5746A, N5747A, N5748A, N5749A, N5750A, N5751A, N5752A, N5761A, N5762A, N5763A, N5764A,
    # Benchview supported N5765A, N5766A, N5767A, N5768A, N5769A, N5770A, N5771A, N5772A, N8731A, N8732A, N8733A, N8734A, N8735A, N8736A, N8737A, N8738A, N8739A, N8740A, N8741A, N8742A,
    # Benchview supported N8754A, N8755A, N8756A, N8757A, N8758A, N8759A, N8760A, N8761A, N8762A, N8920A, N8921A, N8922A, N8923A, N8924A, N8925A, N8926A, N8927A, N8928A, N8929A, N8930A,
    # Benchview supported N8931A, N8932A, N8933A, N8934A, N8935A, N8936A, N8937A, N8940A, N8941A, N8942A, N8943A, N8944A, N8945A, N8946A, N8947A, N8948A, N8949A, N8950A, N8951A, N8952A,
    # Benchview supported N8953A, N8954A, N8955A, N8956A, N8957A, N6731B, N6732B, N6733B, N6734B, N6735B, N6736B, N6741B, N6742B, N6743B, N6744B, N6745B, N6746B, N6773A, N6774A, N6775A,
    # Benchview supported N6776A, N6777A, N6751A, N6752A, N6753A, N6754A, N6755A, N6756A, N6761A, N6762A, N6763A, N6764A, N6765A, N6766A, N6781A, N6782A, N6784A, N6785A, N6786A, N6783A-BAT, N6783A-MFG


}
