# print(f'Invoking __init__.py for {__name__}')


from .HP33120A import HP33120A
from .HP8116A import HP8116A


REGISTER = {
    'HEWLETT-PACKARD,33120A': HP33120A,
    'HEWLETT-PACKARD,8116A,NO_IDN': HP8116A,
}

'''

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
        print(f"Amplitude: {self.amplitude}")
        print(f"Frequency: {self.frequency}")
        print(f"Shape: {self.shape}")
        print(f"Load: {self.load}")
        # print("Output: {}".format(self.output))

    def start(self, lvl=-50):
        """."""
        pass
        # self.amplitude = lvl


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
        self.write(f"SOURce:FREQuency {frequency:.4f}")

    @property
    def shape(self):
        """."""
        return self.query("SOURce:FUNCtion:SHAPe?")

    @shape.setter
    def shape(self, shape="SIN"):
        # SIN|SQU|TRI|RAMP|NOIS|DC|USER
        self.write(f"SOURce:FUNCtion:SHAPe {shape}")

    @property
    def load(self):
        """."""
        return self.query("OUTPut:LOAD?")

    @load.setter
    def load(self, load="INF"):
        # 50 | INF | MAX | MIB
        self.write(f"OUTPut:LOAD {load}")

    @property
    def amplitude(self):
        """VPP|VRMS|DBM|DEF."""
        self.query("SOURce:VOLTage:UNIT?")
        return float(self.query("SOURce:VOLTage?"))
        # return(self.query("SOURce:VOLTage:UNIT?"))

    @amplitude.setter
    @AmplitudeLimiter
    def amplitude(self, amplitude, unit="VPP"):
        self.write(f"SOURce:VOLTage {amplitude:.6f}{unit}")


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
        self.write(f"SOURce:FREQuency {frequency:.4f}")

    @property
    def shape(self):
        """."""
        return self.query("SOURce:FUNCtion:SHAPe?")

    @shape.setter
    def shape(self, shape="SIN"):
        # SIN|SQU|TRI|RAMP|NOIS|DC|USER
        self.write(f"SOURce:FUNCtion:SHAPe {shape}")

    @property
    def load(self):
        """."""
        return self.query("OUTPut:LOAD?")

    @load.setter
    def load(self, load="INF"):
        # 50 | INF | MAX | MIB
        self.write(f"OUTPut:LOAD {load}")

    @property
    def amplitude(self):
        """VPP|VRMS|DBM|DEF."""
        self.query("SOURce:VOLTage:UNIT?")
        return float(self.query("SOURce:VOLTage?"))
        # return(self.query("SOURce:VOLTage:UNIT?"))

    @amplitude.setter
    @AmplitudeLimiter
    def amplitude(self, amplitude, unit="VPP"):
        self.write(f"SOURce:VOLTage {amplitude:.6f}{unit}")


REGISTER = {
    "HEWLETT-PACKARD,33120A,": HP33120A,
    
    'Keysight33500B': Keysight33500B,
    # Benchview suppored 33210A, 33220A, 33250A, 33521A, 33522A, 33509B,
    # 33510B, 33511B, 33512B, 33519B, 33520B, 33521B, 
    # 33522B, 33611A, 33612A, 33621A, 33622A, 81150A, 81160A
}

'''
