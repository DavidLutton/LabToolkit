from ..IEEE488 import IEEE488


class TTI1705(IEEE488):
    """TTI 1705."""

    def __post__(self):
        self.inst.read_termination = '\r\n'

    @property
    def reading(self):
        """."""
        read = self.query_float('READ?')
        if 'OVLOAD' in read:
            return read
        else:
            return float(read[0:10]), read[10:].strip()
