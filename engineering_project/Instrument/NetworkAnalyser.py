#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument

try:
    from Instrument.IEEE488 import IEEE488 as IEEE488
except ImportError:
    from IEEE488 import IEEE488 as IEEE488


class NetworkAnalyser(GenericInstrument, IEEE488):
    """Parent class for NetworkAnalysers."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)


class AgilentE8357A(NetworkAnalyser):
    """HP E8357A.

    .. figure::  images/NetworkAnalyser/AgilentE8357A.jpg
    """


class HP4395A(NetworkAnalyser):
    """HP 4395A.

    .. figure::  images/NetworkAnalyser/HP4395A.jpg
    """

    @property
    def points(self):
        """Sweep Points, max 801."""
        return float(self.write("POIN?"))

    @points.setter
    def points(self, points=801):
        self.write("POIN {}".format(int(points)))

    @property
    def bandwidth(self):
        """IF Bandwidth.

        2, 10, 30, 100, 300, 1000 (=1k), 3000 (=3k), 10000 (=10k), 30000 (=30k)
        """
        return float(self.write("BW?"))

    @bandwidth.setter
    def bandwidth(self, points=1000):
        self.write("BW {}HZ".format(int(points)))

    @property
    def form(self):
        """Format.

        LOGM, PHAS, DELA, LINM, SWR, REAL, IMAG, SMITH, POLA, EXPP, ADMIT, SPECT, NOISE, LINY
        """
        return float(self.write("FMT?"))

    @form.setter
    def form(self, form='LOGM'):
        self.write("FMT {}".format(form))

    @property
    def sweepformat(self):
        """Format.

        LOGF, LINF, LIST, POWE
        Log frequency (Network and impedance analyzers only)
        """
        return float(self.write("SWPT?"))

    @sweepformat.setter
    def sweepformat(self, form='LOGF'):
        self.write("SWPT {}".format(form))

    @property
    def paramater(self):
        """Measure paramater.

        AR, RB, R, A, B, S11, S12, S21, S22, IMAG, IPH, IRE, IIM, AMAG, APH, ARE, AIM, RCM, RCPH, RCM, RCPH, RCR, RCIM, CP, CS, LP, LS, D, Q, RP, RS
        """
        return float(self.write("MEAS?"))

    @paramater.setter
    def paramater(self, paramater='S11'):
        self.write("MEAS {}".format(paramater))

    @property
    def attenuationr(self):
        """Port attenuation R dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.write("ATTR?"))

    @attenuationr.setter
    def attenuationr(self, attenuation=20):
        self.write("ATTR {}DB".format(int(attenuation)))

    @property
    def attenuationa(self):
        """Port attenuation A dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.write("ATTA?"))

    @attenuationa.setter
    def attenuationa(self, attenuation=20):
        self.write("ATTA {}DB".format(int(attenuation)))

    @property
    def attenuationb(self):
        """Port attenuation B dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.write("ATTB?"))

    @attenuationb.setter
    def attenuationb(self, attenuation=20):
        self.write("ATTB {}DB".format(int(attenuation)))

    @property
    def sourcepower(self):
        """Source power dBm."""
        return float(self.write("POWE?"))

    @sourcepower.setter
    def sourcepower(self, power=0):
        self.write("POWE {}".format(int(power)))

    @property
    def start(self):
        """Start frequency."""
        return float(self.write("STAR?"))

    @start.setter
    def start(self, frequency):
        self.write("STAR {}".format(frequency))

    @property
    def stop(self):
        """Stop frequency."""
        return float(self.write("STOP?"))

    @stop.setter
    def stop(self, frequency):
        self.write("STOP {}".format(frequency))

    def trace(self):
        """Get formatted trace."""
        return NotImplemented


class Wiltron360(NetworkAnalyser):
    """Wiltron 360.

    .. figure::  images/NetworkAnalyser/Wiltron360.jpg
    """


class KeysightFieldFox(NetworkAnalyser):
    """Keysight FieldFox.

    .. figure::  images/NetworkAnalyser/KeysightFieldFoxN9928A.jpg
    """

    def __init__(self, instrument, logger=None):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.freqs = [30e3, 26.5e9]
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        # assert self.IDN.startswith('Agilent Technologies, E4440A,')
        self.write("*CLS")  # clear error status

    @property
    def points(self):
        """."""
        return(self.query("SENS:SWE:POIN?"))

    @points.setter
    def points(self, points):
        self.write("SENS:SWE:POIN {0:.0f}".format(points))

    @property
    def start(self):
        """."""
        return(self.query("SENS:FREQ:STAR?"))

    @start.setter
    def start(self, start):
        self.write("SENS:FREQ:STAR {0:.0f}".format(start))

    @property
    def stop(self):
        """."""
        return(self.query("SENS:FREQ:STOP?"))

    @stop.setter
    def stop(self, stop):
        self.write("SENS:FREQ:STOP {0:.0f}".format(stop))

    @property
    def ifbw(self):
        """."""
        return(self.query(":BWID?"))

    @ifbw.setter
    def ifbw(self, start):
        self.write(":BWID {0:.0f}".format(ifbw))

    @property
    def display(self):
        """."""
        return(self.query("DISP:ENAB?"))

    @display.setter
    def display(self, display):
        self.write("DISP:ENAB {:d}".format(display))

    @property
    def trigger(self):
        """."""
        return(self.query("INIT:CONT?"))

    @trigger.setter
    def trigger(self, trigger):
        self.write("INIT:CONT {:d}".format(trigger))

    @property
    def format(self):
        """."""
        return(self.query("CALC:SEL:FORM?"))

    @format.setter
    def format(self, form):
        self.write("CALC:SEL:FORM {}".format(form))

    @property
    def sparameter(self):
        """."""
        return(self.query("CALC:PAR1:DEF?"))

    @sparameter.setter
    def sparameter(self, sparameter="S11"):  # S21, S12, S22
        self.write("CALC:PAR1:DEF {}".format(sparameter))

    def sweep(self):
        """."""
        self.write("INIT")
        self.write("*WAI")

    def readRI(self):
        """."""
        self.write("CALC:DATA:SDAT?")
        answer = self.instrument.read_until(b'\n').decode('ascii')
        parsed = answer.strip().split(",")
        real = [float(parsed[i]) for i in range(0, len(parsed), 2)]
        imag = [float(parsed[i]) for i in range(1, len(parsed), 2)]
        return (real, imag)

    def readFormatted(self):
        """."""
        self.write("CALC:DATA:FDAT?")
        answer = self.instrument.read_until(b'\n').decode('ascii')
        parsed = answer.strip().split(",")
        return ([float(x) for x in parsed], [0.0]*len(parsed))
    # topfreq = freq + span/2
    # botfreq = freq - span/2


REGISTER = {
    "Keysight ZZZZZZZ Fieldfox": KeysightFieldFox,
    'HEWLETT-PACKARD,4395A,': HP4395A
}
