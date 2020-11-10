from .SCPISignalGenerator import SCPISignalGenerator
from .helper import SignalGenerator, amplitudelimiter


class HPESG3000A(SCPISignalGenerator, SignalGenerator):
    """HP ESG-3000A 250e3, 3e9.

    .. figure::  images/SignalGenerator/HPESG3000A.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
