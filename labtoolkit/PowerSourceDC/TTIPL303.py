class TTIPL303():
    """."""

    @property
    def volts(self):
        """."""
        return float(self.query('V1?'))

    @property
    def voltsoutput(self):
        """."""
        return float(self.query(f'V{1}O?'))

    @volts.setter
    def volts(self, volts):
        self.write('V1{2.3f}'.format(volts))

    @property
    def current(self):
        """."""
        return float(self.query('I1?'))

    @property
    def currentoutput(self):
        """."""
        return float(self.query(f'I{1}O?'))

    @current.setter
    def current(self, current):
        self.write('I1{1.3f}'.format(current))

    @property
    def output(self):
        """."""
        return bool(self.query('OP1?'))

    @output.setter
    def output(self, boolean=False):
        self.write(f'OP1 {boolean:d}')

    @property
    def config(self):
        """."""
        return self.query('CONFIG?')

    @property
    def currentrange(self):
        """."""
        return int(self.query(f'IRANGE{1}?'))

    @currentrange.setter
    def currentrange(self, currentrange):
        self.write(f'IRANGE{1}{currentrange}')

    @property
    def voltsoverprotect(self):
        """."""
        return(float(self.query(f'OVP{1}?')))

    @property
    def currentoverprotect(self):
        """."""
        return(float(self.query(f'OCP{1}?')))

    # def setLocal(self): 'LOCAL'


