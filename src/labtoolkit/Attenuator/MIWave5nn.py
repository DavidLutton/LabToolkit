
from ..Instrument import Instrument


class MIWave5nn(Instrument):
    """TBC."""

    def __post__(self):
        self.inst.write_termination = ''

    @property
    def attenuation(self):
        return None  # Readback not supported
    
    # @validsteps([3,4,5,6])
    @attenuation.setter
    def attenuation(self, attenuation):
        self.write(f"{attenuation:.0f}")
