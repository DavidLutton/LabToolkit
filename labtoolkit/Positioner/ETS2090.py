from ..Instrument import Instrument
from time import sleep


class ETS2090(Instrument):
    """.
    
    Also EMCO 2090.
    """
    # *OPC? returns immediately 0 moving 1 complete
    
    def __post__(self):
        self.inst.read_termination = '\r\n'
        self.inst.write_termination = '\r\n'
        self.write('N2')  # Set numeric mode 2 (2090 -- xxx.x) 
    
    @property
    def device_type(self):
        """."""
        return self.query('TYP?')

    @property
    def limit_upper(self):
        """."""
        return self.query_float('UL?')

    @limit_upper.setter
    def limit_upper(self, upper_limit):
        self.write(f'UL {upper_limit}')
    
    @property
    def limit_lower(self):
        """."""
        return self.query_float('LL?')

    @limit_lower.setter
    def limit_lower(self, lower_limit):
        self.write(f'LL {lower_limit}')
    
    @property
    def polarization(self):
        """."""
        # 0 vert, 1 horiz
        return 'Vert' if self.query_int('P?') == 0 else 'Horiz'

    @polarization.setter
    def polarization(self, polarization):
        if polarization == 'Horiz':
            self.write(f'PH')
        if polarization == 'Vert':
            self.write(f'PV')
        
    def sweep_up(self):
        """Not yet tested."""
        return self.write('UP')
    
    def sweep_down(self):
        """Not yet tested."""
        return self.write('DW')

    def target_seek(self):
        """."""
        # self.write(f'SK {target}')
        self.write('SK')

    @property
    def target(self):
        """."""
        return self.query_float('TG?')

    @target.setter
    def target(self, target):
        self.write(f'TG {target}')
        
    @property
    def position(self):
        """."""
        return self.query_float('CP')
    
    
    @property
    def local(self):
        """Return to local control."""
        return self.write('RTL')  # works as expected
    
    def sequence(self, sequence=[400,100]*2):
        """."""
        for step, height in enumerate(sequence):
            self.target = height
            self.target_seek()

            while 1 != self.query_bool('*OPC?'):
                print(f'Not done {step}/{len(sequence)}, current {self.position} cm')
                sleep(0.5)
        self.local