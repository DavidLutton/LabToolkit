from ..GenericInstrument import GenericInstrument
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

    def __init__(self, inst):
        super().__init__(inst)
        self._amplitudelimit = 0.1

        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    @property
    def frequency(self):
        """."""
        return(self.query("FREQ:CW?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"FREQ:CW {frequency:.0f}Hz")

    @property
    def amplitude(self):
        """."""
        return(self.query("AMPL:OUT:LEV?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"AMPL:OUT:LEV {amplitude:.1f}DBM")

    @property
    def output(self):
        """."""
        if self.query("AMPL:OUT:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write(f"AMPL:OUT:STATe {boolean:d}")

    @property
    def fmdeviation(self):
        return self.inst.query('FM:DEViation?')

    @fmdeviation.setter
    def fmdeviation(self, deviation):
        self.inst.write(f'FM:DEViation {deviation} Hz')

    @property
    def fmfrequency(self):
        return self.inst.query('FM:FREQuency?')

    @fmfrequency.setter
    def fmfrequency(self, frequency):
        self.inst.write(f'FM:FREQuency {frequency} Hz')

    @property
    def fmmodulation(self):
        """."""
        if self.inst.query('FM:STATe?') == '1':
            return(True)
        else:
            return(False)

    @fmmodulation.setter
    def fmmodulation(self, boolean=False):
        self.inst.write(f'FM:STATe {boolean:d}')

    @property
    def amdepth(self):
        return self.inst.query('AM:DEPth?')

    @amdepth.setter
    def amdepth(self, depth):
        self.inst.write(f'AM:DEPth {depth}')

    @property
    def amfrequency(self):
        return self.inst.query('AM:FREQuency?')

    @amfrequency.setter
    def amfrequency(self, frequency):
        self.inst.write(f'AM:FREQuency {frequency} Hz')

    @property
    def ammodulation(self):
        """."""
        if self.inst.query('AM:STATe?') == '1':
            return(True)
        else:
            return(False)

    @ammodulation.setter
    def ammodulation(self, boolean=False):
        self.inst.write(f'AM:STATe {boolean:d}')

    @property
    def modulation(self):
        """."""
        if self.inst.query('MODulation:STATe?') == '1':
            return(True)
        else:
            return(False)

    @modulation.setter
    def modulation(self, boolean=False):
        # self.inst.write(f'MODulation:STATe {boolean:d}')
        input(f'{boolean} : done? ')
