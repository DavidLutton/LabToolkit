from ..Instrument import Instrument, local_ren
# from ..IEEE488 import IEEE488


class RohdeSchwarzNRVS(Instrument, local_ren):
    """Rohde-Schwarz NRVS.

    .. figure::  images/PowerMeter/RohdeSchwarzNRVS.jpg
    """

    def __post__(self):
        self.inst.read_termination = '\n'
        self.inst.write_termination = ''
        
        # ZV # IDN
        # self.write('C1')  # full preset
        self.write('MR0')  # preset excluding IEEE bus
        # W5 # \n, EOI
        self.write('KA0')
        self.write('B1')  # show correction freq
        self.write('KF1')  # enable freq correction
        # U0 # Watts
        self.write('U1')  # dBm

        self.write('M0')  # Average power
        self.write('N1')  # Without alphaheader

        self.sw_offset_mag = 0
        
        self.local()

        '''
        inst.query('ZV')
        inst.query('Z2')
        inst.query('ST')
        '''

    @property
    def frequency(self):
        """."""
        return self.query_float('Z2')

    @frequency.setter
    def frequency(self, frequency):
        self.write(f'DF{int(frequency)}')

    @property
    def amplitude(self):
        """."""
        # '   DBM   6.94910E+00'
        return self.query_float('X3')
