# from ..GenericInstrument import GenericInstrument
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

    # def modulation_state(self, modulation):
    #     return self.query_bool(f':{modulation}:STATe?')

    def modulation_disable(self, modulation):
        bool_state = False
        state = 'ON' if bool_state else 'OFF'
        return self.write(f'{modulation}:{state}')

    def modulation_enable(self, modulation):
        bool_state = True
        state = 'ON' if bool_state else 'OFF'
        return self.write(f'{modulation}:{state}')
    
    # self._modulations = ['AM1', 'AM2', 'FM1', 'FM2', 'PULM', 'PM']

    @property
    def modulation_output(self):
        return NotImplemented

    @modulation_output.setter
    def modulation_output(self, state):
        bool_state = True
        state = 'ON' if bool_state else 'OFF'
        return self.write(f'MOD:{state}')

    ''' 
    for q in ['MODE?', 'MOD?', 'INTF4?', 'LF?', 'OPER?', 'ELAPSED?', 'ERROR?', '*IDN?', '*OPT?', 'FM?', 'AM?', 'INTF4?']:

    print(f'{q:^10} {DUT.SignalGenerator[0].query(q)}')

  MODE?    :MODE FM1
   MOD?    :MOD:ON
  INTF4?   :INTF4:FREQ 1000.0;INC 1000.0;SIN
   LF?     :LF:GEN;ON
  OPER?    10354.5
 ELAPSED?  10310.0
  ERROR?   0
  *IDN?    MARCONI INSTRUMENTS,2031,119476059,4.005
  *OPT?    0
   FM?     :FM1:DEVN 5000.0;INTF4;OFF;INC 1000.0
   AM?     :AM1:DEPTH 80.0;INTF4;ON;INC 1.0
  INTF4?   :INTF4:FREQ 1000.0;INC 1000.0;SIN
    '''
    @property
    def modulation(self):
        pass
        # TODO

    @modulation.setter
    def modulation(self, modulation):
        if not modulation.dontpresetmodulation:
            pass
            # self.modulation_output = False
            #for mod in self.modulations_enabled:
            #    self.modulation_disable(mod)

        if modulation is None:
            return None  # return is used to end the function here when modulation is None
        # print(modulation.modulation)

        self.write(f':LF:MON OFF;ON')  # AMD for AM ?

        # shape = 'SIN' if {modulation.shape} == 'Sine' else 'TRI'
        shape = 'SIN'
        self.write(f'INTF4:FREQ {modulation.rate};{shape}')

        if modulation.modulation == 'AM':
            modulator = 'AM1'
            self.write(f'MODE {modulator}')
            self.write(f'{modulator}:INTF4')
            self.write(f'{modulator}:DEPTH {modulation.depth}')        
            # self.write(f':AM:WIDeband:STATe {False:d}')  # in manual not accepted command
            self.modulation_enable(modulator)

        if modulation.modulation == 'FM':
            modulator = 'FM1'
            self.write(f'MODE {modulator}')
            self.write(f'{modulator}:INTF4')
            self.write(f'{modulator}:DEVN {modulation.deviation}')
            self.modulation_enable(modulator)

        '''if modulation.modulation == 'Pulse':
            modulator = 'PULM'
            self.write(f':{modulator}:INTernal:FREQuency {modulation.rate}Hz')
            self.write(f':{modulator}:SOURce INT')  # INT|EXT2

            self.write(f':{modulator}:INTernal:FUNCtion:SHAPe {modulation.shape}')   # SQUare|PULSe
            # :PULM:INTernal[1]:FUNCtion:SHAPe?
            # :PULM:SOURce?
            self.modulation_enable(modulator)
        '''

        self.modulation_output = modulation.enable
    
    @property
    def SystemErrorQueue(self):
        """Get System Error Queue.

        :returns: List of errors
        """
        responces = []
        # responce = False
        responce = self.query('ERROR?')

        while responce != '0':
            responces.append(responce)
            responce = self.query('ERROR?')
        return responces