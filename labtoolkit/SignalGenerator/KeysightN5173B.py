
from .SCPISignalGenerator import SCPISignalGenerator
from .helper import SignalGenerator, amplitudelimiter


class KeysightN5173B(SCPISignalGenerator, SignalGenerator):
    """Keysight N5173B 9e3, 40e9.

    .. figure::  images/SignalGenerator/KeysightN5173B.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
