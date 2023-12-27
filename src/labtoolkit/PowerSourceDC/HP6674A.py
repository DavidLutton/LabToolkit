class HP6674A():
    """HP 6674A 0-60V/0-35A, 2000W.

    .. figure::  images/SourceDC/HP6674A.jpg
    """

    @property
    def volt(self):
        """."""
        return self.query_float('VOLT?')
        # self.query_float('CURR?'))

    @volt.setter
    def volt(self, volt):
        self.write(f'VOLT:LEV {volt}')
    
    @property
    def current_limit(self):
        """."""
        return self.query_float('CURR?')
        # self.query_float('CURR?'))
    
    @current_limit.setter
    def current_limit(self, current_limit):
        self.write(f'CURR:LEV {current_limit}')
    
    @property
    def output(self):
        """."""
        return self.query_bool('OUTP:STAT?')

    @output.setter
    def output(self, state):
        self.write(f'OUTP:STAT {state:b}')

    @property
    def measurevolt(self):
        """."""
        return self.query_float('MEAS:VOLT?')
    
    @property
    def measurecurrent(self):
        """."""
        return self.query_float('MEAS:CURR?')

# inst.query('syst:lang?')
# float(inst.query('VOLT:PROT?'))
# inst.write('VOLT:PROT 55')
# inst.query('SYSTem:ERRor?')
## '+0,"No error"'
# inst.query('SYSTem:VERsion?')
# inst.write('OUTP:PROT:CLE')
# float(inst.query('OUTP:PROT:DELAY?'))
# inst.write('OUTP:PROT:DELAY .25')
# inst.query('SOURce:CURRent:PROTection:STATe?')