from ..IEEE488 import IEEE488
from ..SCPI import SCPI

import numpy as np


class AgilentE4404B(IEEE488, SCPI):
    """."""

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

        self.write(':SYST:ERR:VERB 1')
        self.write(':CAL:AUTO 0')

    def profile(self, profile):
        if profile == 'Downconverter':
            self.span = 0
            self.reswb = 3e6

    '''
    inst.write(f':SENS:FREQ:CENT {cf}')
    inst.write(f':SENS:SWE:TIME {(1/rate)*2:.6f}')
    inst.write('INIT:IMM')  # Restart inc AVG
    inst.query('*OPC?')  # is this finished

    xt = np.linspace(0, float(inst.query(':SENS:SWE:TIME?')), int(inst.query(':SENS:SWEEP:POINts?')))
    yt = np.array(inst.query_ascii_values(':TRAC:DATA? TRACE1'))
    '''

    def trace(self):
        # :INST:SEL?
        # SA
        # :SENS:FREQ:STAR?
        # :SENS:BWID:RES?
        # :SENS:BWID:VID?
        # :SENS:SEP:TIME?
        # :DISP:WIND:TRAC:Y:RLEV
        # :DISP:WIND:TRAC:Y:SPAC?
        # LOG
        # :UNIT:POW?
        # DBM
        self.inst.write('FORM:DATA REAL,32')
        self.inst.write('FORM:BORD SWAP')
        # y = np.array(self.inst.query_binary_values('TRAC:DATA? TRACE1'))
        y = self.inst.query_binary_values('TRAC:DATA? TRACE1', container=np.float64)

        if self.span == 0.0:
            x = np.linspace(0, self.query_float(':SENS:SWE:TIME?'), self.query_int(':SENS:SWEEP:POINts?'))
        else:
            x = np.linspace(self.query_float(':SENS:FREQ:STAR?'), self.query_float(':SENS:FREQ:STOP?'), self.query_int(':SENS:SWEEP:POINts?'))
        return x, y

    @property
    def time(self):
        return self.query_float(':SENS:SWE:TIME?')

    @time.setter
    def time(self, time):
        self.write(f':SENS:SWE:TIME {time}')

    @property
    def frequency(self):
        return self.query_float(':SENS:FREQ:CENT?')

    @frequency.setter
    def frequency(self, frequency):
        self.write(f':SENS:FREQ:CENT {frequency}')

    @property
    def span(self):
        return self.query_float(':SENS:FREQ:SPAN?')

    @span.setter
    def span(self, frequency):
        self.write(f':SENS:FREQ:SPAN {frequency}')

    @property
    def reflevel(self):
        return self.query_float(':DISP:WIND:TRAC:Y:SCAL:RLEV?')

    @reflevel.setter
    def reflevel(self, level):
        self.write(f':DISP:WIND:TRAC:Y:SCAL:RLEV {level}')

    @property
    def resbw(self):
        return self.query_float(':SENS:BWID:RES?')

    @resbw.setter
    def resbw(self, frequency):
        self.write(f':SENS:BWID:RES {frequency}')


'''
ana.write(w)

for q in [
    '*IDN?',
    # '*CAL?',
    ':FORM?',
    ':INST:SEL?',
    # ':SENS:FREQ:STAR?',
    # ':SENS:FREQ:STOP?',s
    ':SENS:BWID:RES?',
    ':SENS:BWID:VID?',
    ':SENS:SWE:TIME?',
    # ':DISP:WIND:TRAC:Y:RLEV?',
    # ':DISP:WIND:TRAC:Y:SPAC?',
    # ':DISP:WIND:TRAC:Y:SCAL:PDIV',
    ':UNIT:POW?',
    ':TRACe1:MODE?',
    ':INITiate:CONTinuous?',
    ':SYSTem:ERRor:NEXT?',
    ':OUTPut:STATe?',
    # ':SOURce:CORRection:OFFSet?',
    ':SOURce:POWer:ATTenuation?',
    # ':SOURce:POWer:ATTenuation:AUTO?',
    ':SOURce:POWer:LEVel:IMMediate:AMPLitude?',
    ':SOURce:POWer:MODE?',
    # ':SOURce:POWer:SPAN?',
    # ':SOURce:POWer:STARt?',
    # ':SOURce:POWer:STEP:AUTO?',
    # ':SOURce:POWer:STEP:INCRement?'
    # ':SOURce:POWer:SWEep?',
    ':SOURce:POWer:TRCKing?',
    ':SENS:FREQ:STAR?',
    ':SENS:FREQ:STOP?',
    # ':SENS:FREQ:POINts?',
    ':SENS:FREQ:SPAN?',
]:
    print(f'{q}  :  {ana.query(q)}', end='')
# :SOURce:POWer:TRCKing:PEAK
# :TRACe1|2|3:MODE WRITe|MAXHold|MINHold|VIEW|BLANk'''
