
from .SCPISignalGenerator import SCPISignalGenerator
# from .helper import SignalGenerator, amplitudelimiter
import numpy as np


class AgilentE4438C(SCPISignalGenerator):
    """."""

    def arb_read(self, waveform):
        arb = self.query_binary_values(
            f':MEM:DATA? "{waveform}"',
            datatype='h',
            container=np.float64,
            is_big_endian=True
        )
        return arb.view(np.complex128)
