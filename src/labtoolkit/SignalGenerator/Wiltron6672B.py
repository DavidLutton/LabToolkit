from ..Instrument import Instrument
from .helper import SignalGenerator, amplitudelimiter


class Wiltron6672B(Instrument, SignalGenerator):
    """Wiltron 6672B 40e9, 60e9.

    .. figure::  images/SignalGenerator/Wiltron6672B.jpg
    """

    def __post__(self):
        """."""

        self.amps = [-20, 17]
        self.freqs = [40e9, 60e9]
        # self.siggen.write("*CLS")  # clear error status
        # self.frequency = min(self.freqs)

    @property
    def frequency(self):
        """."""
        return(self.query("OF0"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"F0{frequency:.2f}GH")

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"L0{amplitude:.2f}DM")

    '''@property
    def output(self):
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))
    '''
