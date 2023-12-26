from ..IEEE488 import IEEE488
from .helper import SignalGenerator, amplitudelimiter

# from ..SCPI import SCPI
"""HP 8664A 100e3, 3e9.

    .. figure::  images/SignalGenerator/HP8664A.jpg
    HEWLETT_PACKARD,8664A
            self.amps = [-140, 17]
        self.freqs = [100e3, 3e9]
"""

"""HP 8665B 100e3, 6e9.

    .. figure::  images/SignalGenerator/HP8665B.jpg
    'HEWLETT_PACKARD,8665B')
        self.amps = [-140, 17]
        self.freqs = [100e3, 6e9]

"""

class HP866nX(IEEE488, SignalGenerator):
    """."""

    def __post__(self):
        self._amplitudelimit = 0.1
        
    @property
    def frequency(self):
        """."""
        return self.query_float("FREQ:CW?")

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"FREQ:CW {frequency:.0f}Hz")

    @property
    def amplitude(self):
        """."""
        return self.query_float("AMPL:OUT:LEV?")

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"AMPL:OUT:LEV {amplitude:.1f}DBM")

    @property
    def output(self):
        """."""
        return self.query_bool("AMPL:OUT:STATe?")

    @output.setter
    def output(self, boolean=False):
        self.write(f"AMPL:OUT:STATe {boolean:d}")

    @property
    def fmdeviation(self):
        return self.query_float('FM:DEViation?')

    @fmdeviation.setter
    def fmdeviation(self, deviation):
        self.write(f'FM:DEViation {deviation} Hz')

    @property
    def fmfrequency(self):
        return self.query_float('FM:FREQuency?')

    @fmfrequency.setter
    def fmfrequency(self, frequency):
        self.write(f'FM:FREQuency {frequency} Hz')

    @property
    def fmmodulation(self):
        """."""
        return self.query_bool('FM:STATe?') 

    @fmmodulation.setter
    def fmmodulation(self, boolean=False):
        self.write(f'FM:STATe {boolean:d}')

    @property
    def amdepth(self):
        return self.query_float('AM:DEPth?')

    @amdepth.setter
    def amdepth(self, depth):
        self.write(f'AM:DEPth {depth}')

    @property
    def amfrequency(self):
        return self.query_float('AM:FREQuency?')

    @amfrequency.setter
    def amfrequency(self, frequency):
        self.write(f'AM:FREQuency {frequency} Hz')

    @property
    def ammodulation(self):
        """."""
        return self.query_bool('AM:STATe?')

    @ammodulation.setter
    def ammodulation(self, boolean=False):
        self.write(f'AM:STATe {boolean:d}')

    @property
    def modulation(self):
        """."""
        return self.query_bool('MODulation:STATe?')

    @modulation.setter
    def modulation(self, boolean=False):
        # self.inst.write(f'MODulation:STATe {boolean:d}')
        input(f'{boolean} : done? ')
