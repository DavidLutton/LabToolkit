from ..IEEE488 import IEEE488


class HP85645A(IEEE488):
    """."""

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        # self.amps = [-60, -2]
        # self.freqs = [300e3, 26.5e9]

    '''
'HEWLETT-PACKARD,85645A,3407A00241,920427'  # E380
>>> source.inst.write('*CLS')
(5, <StatusCode.success: 0>)
>>> source.inst.query('SOURce:FREQuency:MODE?')
'CW'
>>> source.inst.query('SOURce:FREQuency:OFFSet?')
'-3.10700000E+008'
>>> source.inst.query('SOURce:FREQuency:OFFSet:STEP:INCRement?')
'+1.00000000E+003'
>>> source.inst.query('SOURce:ROSCillator:SOURce?')
'+1'
>>> source.inst.query('SOURce:SWEep:RSELect?')
'HP8563E'
>>> source.inst.query('SOURce:FREQuency:STEP:AUTO?')
'+1'
>>> source.inst.query('SOURce:POWer:STEP:INCRement?')
'+1.00000000E-001'
>>> source.inst.query('SOURce:FREQuency:STEP:INCRement?')
'+5.00000000E+007'
>>> source.inst.query('SOURce:POWer:ATTenuation?')
'+0'
>>> source.inst.query('SOURce:POWer:CENTer?')
'-5.10000000E+000'
>>> source.inst.query('SOURce:FREQuency:CW?')
'+1.33500000E+010'
>>> source.inst.query('OUTPut:COUPling?')
'AC'
>>> source.inst.query('OUTPut:STATe?')
'+0'
>>>
    '''

    @property
    def OUTPut_COUPling(self):
        return self.query('OUTPut:COUPling?')

    @OUTPut_COUPling.setter
    def OUTPut_COUPling(self, COUPling):
        self.write(f'OUTPut:COUPling {COUPling}')

    @property
    def frequency(self):
        """."""
        return self.query_float("SOURce:FREQuency:CW?")

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"SOURce:FREQuency:CW {frequency:.0f} Hz")

    @property
    def amplitude(self):
        """."""
        return self.query_float("SOURce:POWer:CENTer?")

    @amplitude.setter
    def amplitude(self, amplitude):
        self.write(f"SOURce:POWer:CENTer {amplitude:.2f} DBM")

    @property
    def output(self):
        """."""
        if self.query("OUTPut:STATe?") == "+1":
            return True
        else:
            return False

    @output.setter
    def output(self, boolean=False):
        self.write(f"OUTPut:STATe {boolean:d}")
