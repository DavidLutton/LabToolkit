from .SCPISignalGenerator import SCPISignalGenerator
from .helper import SignalGenerator, amplitudelimiter


class HPESG3000A(SCPISignalGenerator, SignalGenerator):
    """HP ESG-3000A 250e3, 3e9.

    .. figure::  images/SignalGenerator/HPESG3000A.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
        self._modulations = ['AM1', 'AM2', 'FM1', 'FM2', 'PULM', 'PM']

    @property
    def modulation(self):
        return self.modulations_enabled
        # TODO

    @modulation.setter
    def modulation(self, modulation):
        
        if not modulation.dontpresetmodulation:
            self.modulation_output = False
            for mod in self.modulations_enabled:
                self.modulation_disable(mod)

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
