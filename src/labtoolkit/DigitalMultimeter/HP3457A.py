from ..IEEE488 import IEEE488


class HP3457A(IEEE488):
    
    def __post__(self):
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\r\n'
        # self.write('OFORMAT ASCII')
    
    @property
    def reading(self):
        return self.query_float('?')

