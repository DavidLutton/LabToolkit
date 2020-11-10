from .SCPISignalGenerator import SCPISignalGenerator
from .helper import SignalGenerator, amplitudelimiter


class AgilentN5181A(SCPISignalGenerator, SignalGenerator):
    """Agilent N5181A 100e3, 1,3,6e9.

    .. figure::  images/SignalGenerator/AgilentN5181A.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self._modulations = ['AM', 'FM', 'PULM', 'PM']

    @property
    def modulation(self):
        return self.modulations_enabled
        # TODO

    @modulation.setter
    def modulation(self, modulation):
        self.modulation_output = False

        for mod in self.modulations_enabled:
            self.modulation_disable(mod)

        if modulation is None:
            return None  # return is used to end the function here when modulation is None
        # print(modulation.modulation)

        if modulation.modulation == 'AM':
            modulator = modulation.modulation
            self.write(f':{modulator}:SOURce INT')
            self.write(f':{modulator}:DEPTh {modulation.depth}PCT')
            self.write(f':{modulator}:INTernal:FREQuency {modulation.rate}Hz')
            self.write(f':{modulator}:INTernal:FUNCtion:SHAPe {modulation.shape}')
            # self.write(f':AM:WIDeband:STATe {False:d}')  # in manual not accepted command
            self.modulation_enable(modulator)

        if modulation.modulation == 'FM':
            modulator = modulation.modulation
            self.write(f':{modulator}:INTernal:FREQuency {modulation.rate}Hz')
            self.write(f':{modulator}:DEViation {modulation.deviation}Hz')
            self.modulation_enable(modulator)

        if modulation.modulation == 'Pulse':
            modulator = 'PULM'
            self.write(f':{modulator}:SOURce INT')  # INT|EXT2
            self.write(f':{modulator}:INTernal:FREQuency {modulation.rate}Hz')
            self.write(f':{modulator}:INTernal:FUNCtion:SHAPe {modulation.shape}')   # SQUare|PULSe
            # :PULM:INTernal[1]:FUNCtion:SHAPe?
            # :PULM:SOURce?
            self.modulation_enable(modulator)

        self.modulation_output = modulation.enable
