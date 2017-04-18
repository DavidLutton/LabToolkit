#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
from Instrument.IEEE488 import IEEE488 as IEEE488


class NetworkAnalyser(GenericInstrument, IEEE488):
    """Parent class for NetworkAnalysers."""

    def __init__(self, instrument):
        super().__init__(instrument)




class HPE8357A(NetworkAnalyser):
    """HP E8357A."""


class HP4395A(NetworkAnalyser):
    """HP 4395A."""


class KeysightFieldFox(NetworkAnalyser):
    """Keysight FieldFox."""

    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.freqs = [30e3, 26.5e9]
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        # assert self.IDN.startswith('Agilent Technologies, E4440A,')
        self.write("*CLS")  # clear error status

    @property
    def points(self):
        return(self.query("SENS:SWE:POIN?"))

    @points.setter
    def points(self, points):
        self.write("SENS:SWE:POIN {0:.0f}".format(points))

    @property
    def start(self):
        return(self.query("SENS:FREQ:STAR?"))

    @start.setter
    def start(self, start):
        self.write("SENS:FREQ:STAR {0:.0f}".format(start))

    @property
    def stop(self):
        return(self.query("SENS:FREQ:STOP?"))

    @stop.setter
    def stop(self, stop):
        self.write("SENS:FREQ:STOP {0:.0f}".format(stop))

    @property
    def ifbw(self):
        return(self.query(":BWID?"))

    @ifbw.setter
    def ifbw(self, start):
        self.write(":BWID {0:.0f}".format(ifbw))

    @property
    def display(self):
        return(self.query("DISP:ENAB?"))

    @display.setter
    def display(self, display):
        self.write("DISP:ENAB {:d}".format(display))

    @property
    def trigger(self):
        return(self.query("INIT:CONT?"))

    @trigger.setter
    def trigger(self, trigger):
        self.write("INIT:CONT {:d}".format(trigger))

    @property
    def format(self):
        return(self.query("CALC:SEL:FORM?"))

    @format.setter
    def format(self, form):
        self.write("CALC:SEL:FORM {}".format(form))

    @property
    def sparameter(self):
        return(self.query("CALC:PAR1:DEF?"))

    @sparameter.setter
    def sparameter(self, sparameter="S11"):  # S21, S12, S22
        self.write("CALC:PAR1:DEF {}".format(sparameter))

    def sweep(self):
        self.write("INIT")
        self.write("*WAI")

    def readRI(self):
        self.write("CALC:DATA:SDAT?")
        answer = self.instrument.read_until(b'\n').decode('ascii')
        parsed = answer.strip().split(",")
        real = [float(parsed[i]) for i in range(0, len(parsed), 2)]
        imag = [float(parsed[i]) for i in range(1, len(parsed), 2)]
        return (real, imag)

    def readFormatted(self):
        self.write("CALC:DATA:FDAT?")
        answer = self.instrument.read_until(b'\n').decode('ascii')
        parsed = answer.strip().split(",")
        return ([float(x) for x in parsed], [0.0]*len(parsed))
    # topfreq = freq + span/2
    # botfreq = freq - span/2


register = {
    "Keysight ZZZZZZZ Fieldfox": KeysightFieldFox,

}
