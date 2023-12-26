from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class SCPISignalGenerator(IEEE488, SCPI):

    def __post__(self):
        self._modulations = ['AM1', 'FM1', 'PULM', 'PM']

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
        # self._modulations = ['AM1', 'AM2', 'FM1', 'FM2', 'PULM', 'PM']

    @property
    def modulation(self):
        return self.modulations_enabled
        # TODO

    @modulation.setter
    def modulation(self, modulation):
        
        '''
        if not modulation.dontpresetmodulation:
            self.modulation_output = False
            for mod in self.modulations_enabled:
                self.modulation_disable(mod)
        '''
        
        if modulation is None:
            return None  # return is used to end the function here when modulation is None
        # print(modulation.modulation)

        if modulation.modulation == 'AM':
            modulator = 'AM1'
            self.write(f':{modulator}:SOURce INT')
            self.write(f':{modulator}:DEPTh {modulation.depth}PCT')
            self.write(f':{modulator}:INTernal:FREQuency {modulation.rate}Hz')
            self.write(f':{modulator}:INTernal:FUNCtion:SHAPe {modulation.shape}')
            # self.write(f':AM:WIDeband:STATe {False:d}')  # in manual not accepted command
            self.modulation_enable(modulator)

        if modulation.modulation == 'FM':
            modulator = 'FM1'
            self.write(f':{modulator}:INTernal:FREQuency {modulation.rate}Hz')
            self.write(f':{modulator}:DEViation {modulation.deviation}Hz')
            self.modulation_enable(modulator)

        if modulation.modulation == 'Pulse':
            modulator = 'PULM'
            self.write(f':{modulator}:INTernal:FREQuency {modulation.rate}Hz')
            self.write(f':{modulator}:SOURce INT')  # INT|EXT2

            self.write(f':{modulator}:INTernal:FUNCtion:SHAPe {modulation.shape}')   # SQUare|PULSe
            # :PULM:INTernal[1]:FUNCtion:SHAPe?
            # :PULM:SOURce?
            self.modulation_enable(modulator)

        self.modulation_output = modulation.enable