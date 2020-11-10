from ..GenericInstrument import GenericInstrument
from .helper import SignalGenerator, amplitudelimiter


class Wiltron360SS69(GenericInstrument, SignalGenerator):
    """Wiltron 360SS69 10e6, 40e9.

    .. figure::  images/SignalGenerator/Wiltron360SS69.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))

        self.amps = [-140, 17]
        self.freqs = [10e6, 40e9]
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
