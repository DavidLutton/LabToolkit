from .SCPISignalGenerator import SCPISignalGenerator
from .helper import SignalGenerator, amplitudelimiter


class AnritsuMG3710A(SCPISignalGenerator, SignalGenerator):
    """Anritsu MG3710A 100e3, 6e9.

    .. figure::  images/SignalGenerator/AnritsuMG3710A.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
