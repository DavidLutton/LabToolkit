from ..GenericInstrument import GenericInstrument
from .helper import SignalGenerator, amplitudelimiter


class HP8657A(GenericInstrument, SignalGenerator):
    """HP 8657A 100e3, 1040e6.

    .. figure::  images/SignalGenerator/HP8657A.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)

        # self.amps = [-111, 17]
        self.amps = [-143.5, 17]  # HP 8657A, 8657B
        self.freqs = [100e3, 1040e6]

        # self.siggen.write("*CLS")  # clear error status

    @property
    def frequency(self):
        """."""
        return(self.query("FR?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"FR {frequency:.0f}Hz")

    @property
    def amplitude(self):
        """."""
        return(self.query("AP?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"AP {amplitude:.1f}DM")

    @property
    def output(self):
        """."""
        pass

    @output.setter
    def output(self, boolean=False):
        if boolean is False:
            self.write("R2")
        else:
            if boolean is True:
                self.write("R3")
