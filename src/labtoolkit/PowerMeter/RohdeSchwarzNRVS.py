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
        # '   DBM   6.94910E+00' with N0 headers on
        return self.query_float('X3')

    @property
    def calibration_data(self):
        self.write('SI')
        return [self.inst.read().strip() for i in range(1,32)]

    @property
    def calibration_dates(self):
        self.write('S4')
        return [self.inst.read().strip() for i in range(1,6)]

    @property
    def sensor(self):
        # 'NRV-Z5 /  nnnnnnnn/nnnnn.nn.nn                                                    3X'
        return self.query('SP')

    @property
    def setup(self):
        # 'A0,AV09,B1,G1,KA0,KF1,M0,N1,O1,Q0,RG0,RS3,SC1,U 1,W5'
        return self.query('ST')