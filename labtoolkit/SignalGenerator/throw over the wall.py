from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class SCPISignalGenerator(IEEE488, SCPI):

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    @property
    def frequency(self):
        return self.query_float('SOURce:FREQuency:CW?')

    @frequency.setter
    def frequency(self, frequency):
        self.write(f'SOURce:FREQuency:CW {frequency:.2f} Hz')

    @property
    def amplitude(self):
        return self.query_float('SOURce:POWer:LEVel:AMPLitude?')

    @amplitude.setter
    def amplitude(self, amplitude):
        self.write(f'SOURce:POWer:LEVel:AMPLitude {amplitude:.2f} dBm')

    @property
    def output(self):
        return self.query_bool('OUTPut:STATe?')

    @output.setter
    def output(self, boolean=False):
        self.write(f'OUTPut:STATe {boolean:d}')

    @property
    def modulations_enabled(self):
        return [mod for mod in self._modulations if self.modulation_state(mod)]  # pylint: disable=no-member

    def modulation_state(self, modulation):
        return self.query_bool(f':{modulation}:STATe?')

    def modulation_disable(self, modulation):
        return self.write(f':{modulation}:STATe {False:d}')

    def modulation_enable(self, modulation):
        return self.write(f':{modulation}:STATe {True:d}')

    @property
    def modulation_output(self):
        return self.query_bool(':OUTPut:MODulation:STATe?')

    @modulation_output.setter
    def modulation_output(self, state):
        self.write(f':OUTput:MODulation:STATe {state:d}')
