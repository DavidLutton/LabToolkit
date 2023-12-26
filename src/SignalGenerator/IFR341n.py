from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI
from .helper import SignalGenerator, amplitudelimiter


class IFR341n(IEEE488, SignalGenerator):
    """."""

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    @property
    def frequency(self):
        return self.query_float('SOURce:FREQuency:CW?')

    @frequency.setter
    def frequency(self, frequency):
        self.write(f'SOURce:FREQuency:CW {frequency:.0f} Hz')

    @property
    def amplitude(self):
        return self.query_float('SOURce:POWer:LEVel:AMPLitude?')

    @amplitude.setter
    def amplitude(self, amplitude):
        self.write(f'SOURce:POWer:LEVel:AMPLitude {amplitude:.2f} dBm')
