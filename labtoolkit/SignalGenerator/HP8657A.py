from ..Instrument import Instrument
from .helper import SignalGenerator, amplitudelimiter

# GPIB0::4::INSTR
#Generator, 0.1MHz - 1040MHz, -143.5 - 17 dBm, ['CW','AM','FM']
# \Manuals\H\HP_Agilent_Keysight\8\86\8657\08657-91039.pdf P61,62,63,64

class HP8657A(Instrument, SignalGenerator):
    """HP 8657A 100e3, 1040e6.

    .. figure::  images/SignalGenerator/HP8657A.jpg
    """


    # self.amps = [-111, 17]
    # self.amps = [-143.5, 17]  # HP 8657A, 8657B
    # self.freqs = [100e3, 1040e6]

    @property
    def frequency(self):
        """."""
        return self.query_float("FR?")

    @frequency.setter
    def frequency(self, frequency):
        self.write(f'FR {frequency:.2f} Hz')

    @property
    def amplitude(self):
        """."""
        return self.query_float("AP?")

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f'AP {amplitude:.1f} DM')

    @property
    def output(self):
        """."""
        pass

    @output.setter
    def output(self, boolean):
        match boolean:
            case False:
                self.write("R2")
            case True:
                self.write("R3")

    @property
    def modulation_basic(self):
        return NotImplmentedError

    @modulation_basic.setter
    def modulation_basic(self, scheme):
        match scheme[0]:
            case 'AM':
                self.write(f'AM {scheme[1]} PC')
            case 'FM':
                self.write(f'FM {scheme[1]} KZ')
            case _:
                self.write('S4')
                # self.write('S2') # 400 Hz
                # self.write('S3') # 1 kHz
                

