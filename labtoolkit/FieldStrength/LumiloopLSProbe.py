from ..IEEE488 import IEEE488
from ..SCPI import SCPI

class LumiloopLSProbe(IEEE488, SCPI):
    """."""

    def __post__(self):
        pass
        # self.write(f':SYST:ERR:VERB {True:b}')  # Turn on verbose command errors

    @property
    def magnitude(self):
        return self.query_float(':MEASure:FProbe:Efield:MAG?')
    
    @property
    def magnitude_all(self):
        return self.query_ascii_values(':MEASure:FProbe:Efield:ALL?')
        '''
        # '0.0621137,0.0999184,0.107581,0.159422'
        # [E] = sqrt((x**2)+(y**2)+(z**2))
        x, y, z = 0.0621137, 0.0999184, 0.107581
        Emag = np.sqrt((x**2)+(y**2)+(z**2))
        # 0.1594223006585026
        '''
   
    @property
    def frequency(self):
        return self.query_float(':SYSTem:FREQuency?')

    @frequency.setter
    def frequency(self, frequency):
        self.write(f':SYSTem:FREQuency {frequency}')
            
    @property
    def mode(self):
        return self.query_int(':SYSTem:MODE?')

    @mode.setter
    def mode(self, mode):
        self.write(f':SYSTem:MODE {mode:0.0f}')
