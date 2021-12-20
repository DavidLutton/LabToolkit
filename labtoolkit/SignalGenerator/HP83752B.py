from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI
from .helper import SignalGenerator, amplitudelimiter

class HP83752B(IEEE488, SCPI, SignalGenerator):
    """."""

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self._amplitudelimit = 0

    '''
    inst.query('ROSCillator:SOURce?'), inst.query('ROSCillator:SOURce:AUTO?')
    inst.write('ROSCillator:SOURce INTernal')
    inst.write('ROSCillator:SOURce:AUTO 1')
    '''
    @property
    def frequency(self):
        return float(self.inst.query('SOURce:FREQuency:CW?'))

    @frequency.setter
    def frequency(self, frequency):
        self.inst.write(f'SOURce:FREQuency:CW {frequency:.2f} Hz')

    @property
    def amplitude(self):
        return float(self.inst.query('SOURce:POWer:LEVel:AMPLitude?'))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, power):
        self.inst.write(f'SOURce:POWer:LEVel:AMPLitude {power:.2f} DBM')

    @property
    def output(self):
        """."""
        if self.inst.query('OUTPut:STATe?') == '+1':
            return True
        else:
            return False

    @output.setter
    def output(self, boolean=False):
        self.inst.write(f'OUTPut:STATe {boolean:d}')