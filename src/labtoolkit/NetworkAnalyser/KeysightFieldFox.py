from ..IEEE488 import IEEE488
from ..SCPI import SCPI
import numpy as np


class KeysightFieldFox(IEEE488, SCPI):
    """Keysight FieldFox.

    .. figure::  images/NetworkAnalyser/KeysightFieldFoxN9928A.jpg
    """

    def __init__(self, instrument, logger=None):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.freqs = [30e3, 26.5e9]
        # self.log.info('Creating an instance of\t' + str(__class__))

        self.write("*CLS")  # clear error status

    @property
    def points(self):
        """Sweep Points, max 10,001."""
        return(self.query("SENS:SWE:POIN?"))

    @points.setter
    def points(self, points):
        self.write(f"SENS:SWE:POIN {points:.0f}")

    @property
    def start(self):
        """Start frequency."""
        return(self.query("SENS:FREQ:STAR?"))

    @start.setter
    def start(self, start):
        self.write(f"SENS:FREQ:STAR {start:.0f}Hz")

    @property
    def stop(self):
        """Stop frequency."""
        return(self.query("SENS:FREQ:STOP?"))

    @stop.setter
    def stop(self, stop):
        self.write(f"SENS:FREQ:STOP {stop:.0f}Hz")

    @property
    def bandwidth(self):
        """IF bandwidth."""
        return(self.query(":BWID?"))

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        self.write(f":BWID {bandwidth:.0f}")

    @property
    def display(self):
        """."""
        return(self.query("DISP:ENAB?"))

    @display.setter
    def display(self, display):
        self.write(f"DISP:ENAB {display:d}")

    @property
    def trigger(self):
        """."""
        return(self.query("INIT:CONT?"))

    @trigger.setter
    def trigger(self, trigger):
        self.write(f"INIT:CONT {trigger:d}")

    @property
    def format(self):
        """."""
        return(self.query("CALC:SEL:FORM?"))

    @format.setter
    def format(self, form):
        self.write(f"CALC:SEL:FORM {form}")

    @property
    def sparameter(self):
        """."""
        return(self.query("CALC:PAR1:DEF?"))

    @sparameter.setter
    def sparameter(self, sparameter="S11"):  # S21, S12, S22
        self.write(f"CALC:PAR1:DEF {sparameter}")

    def sweep(self):
        """."""
        self.write("INIT")
        self.write("*WAI")

    def readRI(self):
        """."""
        self.write("CALC:DATA:SDAT?")
        answer = self.read(b'\n').decode('ascii')
        parsed = answer.strip().split(",")
        real = [float(parsed[i]) for i in range(0, len(parsed), 2)]
        imag = [float(parsed[i]) for i in range(1, len(parsed), 2)]
        return (real, imag)

    def readFormatted(self):
        """."""
        self.write("CALC:DATA:FDAT?")
        answer = self.read(b'\n').decode('ascii')
        parsed = answer.strip().split(",")
        return ([float(x) for x in parsed], [0.0] * len(parsed))
    # topfreq = freq + span/2
    # botfreq = freq - span/2
