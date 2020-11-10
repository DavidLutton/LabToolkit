from ..IEEE488 import IEEE488
from ..SCPI import SCPI
from .FrequencyCounter import FrequencyCounter


class HP53132A(FrequencyCounter, IEEE488, SCPI):
    """."""

    def __init__(self, inst):
        """."""
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self.inst.timeout = 5000

    '''
    *IDN?
    HEWLETT-PACKARD,53132A,0,4806

    :SENSe:ROSCillator:SOURce?
    EXT


    :SENSe:ROSCillator:SOURce:AUTO?
    1/0

    :SENSe:ROSCillator:SOURce:AUTO OFF

    :READ?
    Single read of float value, trigger becomes single

    :FETCh?
    Fetch of current of float value, trigger remains continuous


    >>> round(10000000.000583 - 10e6, 8)
    '''

    @property
    def frequency(self):
        """."""
        return self.query_float('FETCH:FREQUENCY?')
