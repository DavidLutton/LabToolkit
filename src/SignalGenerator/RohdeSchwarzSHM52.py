from ..Instrument import Instrument
from .helper import SignalGenerator, amplitudelimiter

class RohdeSchwarzSHM52(Instrument, SignalGenerator):
    """Rohde and Schwarz SHM, 100e3-2e9."""

    def __post__(self):
        """."""
        self.amps = [-107, 17]
        self.freqs = [100e3, 2e9]

    @property
    def frequency(self):
        """."""
        return self.query("RF?")

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"RF {frequency:.0f}HZ")

    @property
    def amplitude(self):
        """."""
        return self.query("L:?")

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"LEV {amplitude:.1f}DBM")

    @property
    def output(self):
        """."""
        if self.query("L:?") == "1":
            return True
        else:
            return False

    @output.setter
    def output(self, boolean=False):
        # LEV:OFF
        if boolean is False:
            # self.amplitude = min(self.amps)
            self.write("LEV:OFF")
