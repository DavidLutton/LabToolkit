
from .SCPISignalGenerator import SCPISignalGenerator
from .helper import SignalGenerator, amplitudelimiter


class Agilent83650B(SCPISignalGenerator, SignalGenerator):
    """Agilent 83650B 10e6, 50e9.

    """
    @property
    def amplitude(self):
        return self.query_float(':POWer:LEVel')

    @amplitude.setter
    def amplitude(self, amplitude):
        self.write(f':POWer:LEVel {amplitude:.2f} dBm')
