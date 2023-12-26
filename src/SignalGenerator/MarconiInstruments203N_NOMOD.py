from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class MarconiInstruments203N(IEEE488):
    """MarconiInstruments 203N 10e3.

    10 kHz to 1.35 GHz (2030)
    10 kHz to 2.7 GHz (2031)
    10 kHz to 5.4 GHz (2032)
    """

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.write_termination = '\n'

    '''
    print( write('CFRQ:VALUE 1234.5678912MHZ') )
    MODE?
    MODE AM
    MODE FM
    MOD:ON
    MOD:OFF
    MOD?
    AM:DEPTH
    AM:INTF1
    AM:ON
    AM:OFF
    AM?
    INTF1  ,2,3,4,5,6
    INTF1:FREQ 1KHz
    INTF1:SIN
    INTF1?
    LF?
    LF:ON
    LF:OFF
    LFGF?
    LFGF:VALUE
    LFGF:SIN
    LFGF:TRI
    LFGL?
    LFGL:VALUE
    LFGL:UNITS DBM,DBV,DBMV,V,MV,UV
    SWEEP?
    BACKL:ON
    BACKL:OFF
    TIME?
    DATE?
    OPER? operating hours
    ELAPSED? hours since last reset
    ERROR?
    KLOCK
    KUNLOCK
    '''

    @property
    def frequency(self):
        """."""
        # return(self.query("CFRQ?"))  # ':CFRQ:VALUE 50000000.0;INC 1000.0'
        return float(self.query("CFRQ?").split(';')[0].split(' ')[1])  # ':CFRQ:VALUE 50000000.0;INC 1000.0'

    @frequency.setter
    def frequency(self, frequency):
        self.write("CFRQ:VALUE {0:.1f}Hz".format(frequency))

    @property
    def amplitude(self):
        """."""
        return float((self.query("RFLV?").split(';')[1]).split(' ')[1])

    @amplitude.setter
    # @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("RFLV:VALUE {0:.2f}DBM".format(amplitude))

    @property
    def output(self):
        """."""
        print(self.query("RFLV?"))
        # ':RFLV:UNITS DBM;VALUE -100.0;INC 1.0;OFF'.split(';')[-1]  == 'OFF'

    @output.setter
    def output(self, boolean=False):
        if boolean is True:
            self.write("RFLV:ON")
        else:
            self.write("RFLV:OFF")
