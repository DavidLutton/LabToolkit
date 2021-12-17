from .SCPISignalGenerator import SCPISignalGenerator
from .helper import SignalGenerator, amplitudelimiter


class AgilentE4422B(SCPISignalGenerator, SignalGenerator):
    """Agilent E4422B 250e3, 4e9.

    .. figure::  images/SignalGenerator/AgilentE4422B.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
        if self.query(':SYSTem:LANGuage?') != '"SCPI"':
            self.write(':SYSTem:LANGuage "SCPI"')
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


'''
GEN = rm.open_resource('GPIB0::3::INSTR')
assert GEN.query('*IDN?').startswith('Hewlett-Packard, ESG-4000B, MY41000406, B.03.8')

levelcurrent = float(GEN.query("POWer:LEVel?"))
GEN.write("POWer:LEVel " + str(levelnew) + "dBm")


:DIAGnostic[:CPU]:INFOrmation:OTIMe?

:FREQuency[:CW] <val><unit>
:FREQuency[:CW]?
:FREQuency:MODE CW|FIXed|LIST
:FREQuency:MODE?
:OUTPut:MODulation[:STATe] ON|OFF|1|0
:OUTPut:MODulation[:STATe]?
:OUTPut[:STATe] ON|OFF|1|0
:OUTPut[:STATe]?

:POWer:ATTenuation:AUTO ON|OFF|1|0
:POWer:ATTenuation:AUTO?
:UNIT:POWer DBM|DBUV|V|VEMF|
:UNIT:POWer?
'''
