
from .SCPISignalGenerator import SCPISignalGenerator
from .helper import SignalGenerator, amplitudelimiter


class AgilentN5182A(SCPISignalGenerator, SignalGenerator):
    """Agilent N5182A 100e3, 6e9.

    .. figure::  images/SignalGenerator/AgilentN5182A.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
