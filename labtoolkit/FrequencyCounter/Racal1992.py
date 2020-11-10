from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from .FrequencyCounter import FrequencyCounter


class Racal1992(GenericInstrument, FrequencyCounter):
    """."""

    def __init__(self, inst):
        """."""
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self.inst.timeout = 9000  # to much?

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.inst}")

    '''
    IP preset
    FA Frequency source port a
    SRS10 digits 10
    SRS8 digits 8
    T0 continous trig
    T1 hold wating for trig
    T2 single trig query read
    '''

    @property
    def frequency(self):
        """."""
        return float(self.query('T2', delay=0.1)[3:])

    def preset(self):
        """."""
        self.write('IP')

    def port(self, port):
        """."""
        self.write(f'F{port.upper()}')

    def remote(self):
        """."""
        self.write_list(['SRS10', 'T1'], delay=0.1)

    def local(self):
        """."""
        self.write_list(['SRS8', 'T0'], delay=0.1)

# print(value)  # in Hz
# print(value / 1e6)  # in MHz
# print(round(value / 1e6, 14))  # in MHz
# print(round(value - 50e6, 8))  # in Hz error from nominal 50MHz
