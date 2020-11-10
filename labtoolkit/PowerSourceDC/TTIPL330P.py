class TTIPL330P():
    """TTI PL330P 0-32V/0-3A.

    IDN: THURLBY-THANDAR,PL330P,0,1.10

    .. figure::  images/SourceDC/TTIPL330P.jpg
    """

    '''
-> *IDN?
<- THURLBY-THANDAR,PL330P,0,1.10

-> V1?
<- V1 0.00

-> I1?
<- I1 0.001

-> *LRN?
<- I1 0.001;V1 0.00;OP1 0;DELTAV1 0.01;DELTAI1 0.001;DAMPING1 1

-> V1 5
-> V1?
<- V1 5.00


-> I1 5

-> I1?
<- I1 1.000

-> *LRN?
<- I1 0.001;V1 0.00;OP1 0;DELTAV1 0.01;DELTAI1 0.001;DAMPING1 1

-> OP1 1
  Output on
-> OP1 0
  Output off


http://forums.ni.com/ni/attachments/ni/170/181751/1/PL-P%20Instruction%20Manual.pdf


http://www.tti-test.com/downloads/drivers-download.htm
    '''

    @property
    def volts(self):
        """."""
        self.query('V1?')

    @volts.setter
    def volts(self, volts):
        self.write(f'V1{volts}')

    @property
    def current(self):
        """."""
        self.query('I1?')

    @current.setter
    def current(self, current):
        self.write(f'I1{current}')

    @property
    def output(self):
        """."""
        self.query('OP1?')

    @output.setter
    def output(self, boolean=False):
        self.write(f'OP1 {boolean:d}')