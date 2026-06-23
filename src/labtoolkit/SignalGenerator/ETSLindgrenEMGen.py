from ..Instrument import Instrument

# from .helper import SignalGenerator, amplitudelimiter


class ETSLindgrenEMGen(Instrument):
    """ETS Lindgren EMGen.

    .. figure::  images/SignalGenerator/TODO.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self.slot = 6

    @property
    def output(self):
        """."""
        return self.query_bool(f'{self.slot}:OUTPut:STATe?')

    @output.setter
    def output(self, boolean=False):  ## ??? exact response
        flag = 'ON' if boolean == True else 'OFF'
        self.write(f'{self.slot}:OUTPut{1}:STATe {flag}')

    @property
    def frequency(self):
        return float(self.query(f'{self.slot}:FREQuency?').split(' ')[1])

    @frequency.setter
    def frequency(self, frequency):
        self.write(f'{self.slot}:FREQuency {frequency:.0f} Hz')

    @property
    def amplitude(self):
        return float(self.query(f'{self.slot}:POWer?').split(' ')[1])

    @amplitude.setter
    def amplitude(self, amplitude):
        self.write(f'{self.slot}:POWer {amplitude:.2f} DBM')
