from ..Instrument import Instrument


class HP8116A(Instrument):
    """HP 8116A, 0 to 50MHz.

    .. figure::  images/WaveformGenerator/HP8116A.jpg
    """
    """."""

    # self.amps = [0.01, 7]
    # self.freqs = [0, 50e6]

    # ' NO MESSAGE' or ' SYNTAX' on inital or following comms

    def __post__(self):
        self.inst.read_termination = '\r\n'
        self.inst.write_termination = '\r\n'

    def state(self):
        """."""
        print(f"Amplitude: {self.amplitude}")
        print(f"Frequency: {self.frequency}")
        print(f"Shape: {self.shape}")
        # print(f"Load: {self.load}")
        # print("Output: {}".format(self.output))

    @property
    def frequency(self):
        """."""
        return self.query("IFRQ")

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"FRQ {frequency} Hz")
 
    @property
    def shape(self):
        """."""
        # inst.query('W3') # 0, 1,2,3 DC, Sine, Tri, Square
        return NotImplementedError # self.query("SOURce:FUNCtion:SHAPe?")

    @shape.setter
    def shape(self, shape="SIN"):
        # self.write(f"SOURce:FUNCtion:SHAPe {shape}")
        pass

    @property
    def amplitude(self):
        return self.query("IAMP")

    @amplitude.setter
    # @AmplitudeLimiter
    def amplitude(self, amplitude):
        self.write(f"AMP {amplitude} V")

    @property
    def offset(self):
        return self.query("IOFS")

    # @AmplitudeLimiter
    @offset.setter
    def offset(self, amplitude):
        self.write(f"OFS {amplitude} V")

    @property
    def setup(self):
        # ' M1,CT0,T0,W0,H0,A0,L0,C0,D0,FRQ 55.0 HZ,DTY   50  %,WID 500  MS,AMP 1.00  V,OFS 7.50  V,'
        setup_str = self.query('CST').strip()
        # 'M1,CT0,T0,W0,H0,A0,L0,C0,D0,FRQ 55.0 HZ,DTY   50  %,WID 500  MS,AMP 1.00  V,OFS 7.50  V,'
        
        flags = [x for x in setup_str.split(',') if len(x) == 2 or len(x) == 3]
        # ['M1', 'CT0', 'T0', 'W0', 'H0', 'A0', 'L0', 'C0', 'D0']

        values = [x for x in setup_str.split(',') if len(x) > 3]
        # ['FRQ 55.0 HZ', 'DTY   50  %', 'WID 500  MS', 'AMP 1.00  V', 'OFS 7.50  V']
        return setup_str
        