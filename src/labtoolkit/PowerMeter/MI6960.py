from ..Instrument import Instrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class MI6960(Instrument):
    
    """."""
    def __post__(self):
        self.inst.read_termination = '\r\n'
        self.inst.write_termination = '\n'
    
        # self.inst.write('RE')  # Reset
        # time.sleep(1)
        # self.calfactor = 100
        # self.linearityfactor = 10.0
        # self.offset = 0.0
        # self.reference = 1
    
    # UN 0 dBm, 1 Watts
    # inst.query('?')  # 'VBD-0886E-03'
    # inst.query('RS').split(',')  # '6960B,UN0,DR-0000E+00,SR2,AV+2000E-02,LF+8000E-03,DC+1000E-01,CF+1000E-01,PR1,TR00,SQ0,RF0,HF0,AA1,PU1,PK0,IS3'
    # float(inst.query('RS').split(',')[7][2:])  # 100
    # inst.query('RC')  # 'AZ+2121E+00,AC+3195E+00,OA+1800E-02,OB+4500E-02,OC+2300E-02,OD+2300E-02,OE+2200E-02'
    # float(inst.query('?')[3:])
    # inst.read()

    # inst.write('AC')
    # inst.write('AZ')
    
    def calibrate(self):
        self.inst.write('AZ, AC')  # requires lin f and cal f

    @property
    def settings(self):
        return self.inst.query('RS').split(',')  # '6960B,UN0,DR-0000E+00,SR2,AV+2000E-02,LF+8000E-03,DC+1000E-01,CF+1000E-01,PR1,TR00,SQ0,RF0,HF0,AA1,PU1,PK0,IS3'
        
    @property
    def calfactor(self):
        return NotImplemented
    
    @calfactor.setter
    def calfactor(self, calfactor):
        self.inst.write(f'CF{calfactor}E')
        
    @property
    def offset(self):
        return NotImplemented
    
    @offset.setter
    def offset(self, offset):
        self.inst.write(f'DR{offset}E')  # 0.0 okay, 0 not accepted
        
    @property
    def linearityfactor(self):
        return NotImplemented
    
    @linearityfactor.setter
    def linearityfactor(self, linearityfactor):  # 0.1 to 14.99
        self.inst.write(f'LF{linearityfactor}E')  # int

    @property
    def averages(self):
        return NotImplemented
    
    @averages.setter
    def averages(self, averages):
        self.inst.write(f'AV{averages}E') 
    
    @property
    def reference(self):  # Power Reference
        return NotImplemented
    
    @reference.setter
    def reference(self, reference):
        self.inst.write(f'PR{reference}')         
    
    @property
    def power(self):
        self.inst.write('TR00')  # soft reset of measurand 
        return float(self.inst.query('?', delay=10)[3:])  # 'VBD-0886E-03'  # ? works but still causes error 07 command error
        
