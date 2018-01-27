#!/usr/bin/env python3

"""WaveformGenerator Instrument classes."""

# import time
# import logging
# import pint

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI
from labtoolkit.Utils import AmplitudeLimiter


class WaveformGenerator(GenericInstrument):
    """WaveformGenerator SCPI."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # super().__init__(instrument)

    def safe(self):
        """."""
        pass
        # self.amplitude = min(self.amps)
        # self.frequency = min(self.freqs)
        # self.output = False

    def state(self):
        """."""
        print("Amplitude: {}".format(self.amplitude))
        print("Frequency: {}".format(self.frequency))
        print("Shape: {}".format(self.shape))
        print("Load: {}".format(self.load))
        # print("Output: {}".format(self.output))

    def start(self, lvl=-50):
        """."""
        pass
        # self.amplitude = lvl


class HP33120A(WaveformGenerator):
    """HP 33120A, 0 to 15MHz.

    .. figure::  images/WaveformGenerator/HP33120A.jpg
    """

    def __repr__(self):
        """."""
        return "{}, {}".format(__name__, self.instrument)

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.amplimit = 5
        # self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('HEWLETT-PACKARD,???,')
        self.amps = [0.01, 5]
        self.freqs = [0, 15e6]

        # self.siggen.write("*CLS")  # clear error status

        # self.safe()
        # self.state()

    @property
    def frequency(self):
        """."""
        return float(self.query("SOURce:FREQuency?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("SOURce:FREQuency {0:.4f}".format(frequency))

    @property
    def shape(self):
        """."""
        return self.query("SOURce:FUNCtion:SHAPe?")

    @shape.setter
    def shape(self, shape="SIN"):
        # SIN|SQU|TRI|RAMP|NOIS|DC|USER
        self.write("SOURce:FUNCtion:SHAPe {}".format(shape))

    @property
    def load(self):
        """."""
        return self.query("OUTPut:LOAD?")

    @load.setter
    def load(self, load="INF"):
        # 50 | INF | MAX | MIB
        self.write("OUTPut:LOAD {}".format(load))

    @property
    def amplitude(self):
        """VPP|VRMS|DBM|DEF."""
        self.query("SOURce:VOLTage:UNIT?")
        return float(self.query("SOURce:VOLTage?"))
        # return(self.query("SOURce:VOLTage:UNIT?"))

    @amplitude.setter
    @AmplitudeLimiter
    def amplitude(self, amplitude, unit="VRMS"):
        self.write("SOURce:VOLTage:UNIT {}".format(unit))
        self.write("SOURce:VOLTage {0:.6f}".format(amplitude))


class HP8116A(WaveformGenerator):
    """HP 8116A, 0 to 50MHz.

    .. figure::  images/WaveformGenerator/HP8116A.jpg
    """

    @property
    def frequency(self):
        """."""
        return float(self.query("SOURce:FREQuency?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("SOURce:FREQuency {0:.4f}".format(frequency))

    @property
    def shape(self):
        """."""
        return self.query("SOURce:FUNCtion:SHAPe?")

    @shape.setter
    def shape(self, shape="SIN"):
        # SIN|SQU|TRI|RAMP|NOIS|DC|USER
        self.write("SOURce:FUNCtion:SHAPe {}".format(shape))

    @property
    def load(self):
        """."""
        return self.query("OUTPut:LOAD?")

    @load.setter
    def load(self, load="INF"):
        # 50 | INF | MAX | MIB
        self.write("OUTPut:LOAD {}".format(load))

    @property
    def amplitude(self):
        """VPP|VRMS|DBM|DEF."""
        self.query("SOURce:VOLTage:UNIT?")
        return float(self.query("SOURce:VOLTage?"))
        # return(self.query("SOURce:VOLTage:UNIT?"))

    @amplitude.setter
    @AmplitudeLimiter
    def amplitude(self, amplitude, unit="VPP"):
        self.write("SOURce:VOLTage {0:.6f}{1}".format(amplitude, unit))


class Keysight33500B(WaveformGenerator):
    """Keysight 33500B, 0 to 20MHz.

    .. figure::  images/WaveformGenerator/Keysight33500B.jpg
    """

    @property
    def frequency(self):
        """."""
        return float(self.query("SOURce:FREQuency?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("SOURce:FREQuency {0:.4f}".format(frequency))

    @property
    def shape(self):
        """."""
        return self.query("SOURce:FUNCtion:SHAPe?")

    @shape.setter
    def shape(self, shape="SIN"):
        # SIN|SQU|TRI|RAMP|NOIS|DC|USER
        self.write("SOURce:FUNCtion:SHAPe {}".format(shape))

    @property
    def load(self):
        """."""
        return self.query("OUTPut:LOAD?")

    @load.setter
    def load(self, load="INF"):
        # 50 | INF | MAX | MIB
        self.write("OUTPut:LOAD {}".format(load))

    @property
    def amplitude(self):
        """VPP|VRMS|DBM|DEF."""
        self.query("SOURce:VOLTage:UNIT?")
        return float(self.query("SOURce:VOLTage?"))
        # return(self.query("SOURce:VOLTage:UNIT?"))

    @amplitude.setter
    @AmplitudeLimiter
    def amplitude(self, amplitude, unit="VPP"):
        self.write("SOURce:VOLTage {0:.6f}{1}".format(amplitude, unit))


REGISTER = {
    "HEWLETT-PACKARD,33120A,": HP33120A,
    'HP8116A': HP8116A,
    'Keysight33500B': Keysight33500B,
    # Benchview suppored 33210A, 33220A, 33250A, 33521A, 33522A, 33509B,33510B, 33511B, 33512B, 33519B, 33520B, 33521B, 33522B, 33611A, 33612A, 33621A, 33622A, 81150A, 81160A
}
