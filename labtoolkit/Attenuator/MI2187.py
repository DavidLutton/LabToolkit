
from ..IEEE488 import IEEE488


class MI2187(IEEE488):
    """Marconi Instruments 2187 - DC-20GHz 1W max N-type.

    .. figure::  images/Attenuator/MI2187.jpg
    """

    def __post__(self):
        self._set_points = [
            0, 3, 6, 144,
        ]  # TODO get list of and check setting valid set points

    @property
    def attenuation(self):
        """Set Attenuation."""
        return float(self.query("ATTN?"))

    # @validsteps([3,4,5,6])
    @attenuation.setter
    def attenuation(self, attenuation):
        # if attenuation in self.attenuations:
        self.write(f"ATTN {attenuation:.0f}DB")

    def preset(self):
        self.attenuation = 144
