from ..IEEE488 import IEEE488
from ..SCPI import SCPI
from dataclasses import dataclass


class ELVA1DPM(IEEE488):
    """ELVA1 DPM.

    """
    @dataclass
    class Reading:
        """Class for holding a reading from a powermeter."""
        Unit: str
        Amplitude: float
    
    @property
    def frequency(self):
        """Frequency used for correction factor lookup."""
        return self.frequency_

    @frequency.setter
    def frequency(self, freq):
        self.frequency_ = freq

    @property
    def amplitude(self):
        GHz = self.frequency / 1e9
        ret = self.query(f'{GHz:06.2f}', delay=1) 
        
        read = self.Reading(
            Unit='TBC',
            Amplitude=float(ret.split(' ')[1])
        )
        return read.Amplitude

