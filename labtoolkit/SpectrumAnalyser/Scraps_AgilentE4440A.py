from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI

import numpy as np


class AgilentE4440A(IEEE488, SCPI):

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    def configure(self):
        self.referenceoutput = True
        self.frequencyspan = 1e3
        self.resolutionbandwidth = 1e3
        # self.write(":RBW 1kHz")
        # self.write(":BAND 1kHz")
        # self.write(":FREQuency:SPAN 1KHz")

    @property
    def measurement(self, *, marker=1):
        """Set instrument marker to peak and read X, Y."""
        self.write(":CALCulate:MARKer{}:STATe 1".format(marker))
        self.write(":CALCulate:MARKer{}:MAX".format(marker))

        amplitude = self.query_float(f":CALCulate:MARKer{marker}:Y?")  # AMP
        frequency = self.query_float(f":CALCulate:MARKer{marker}:X?")  # FREQ

        # return(float(freqmeas), float(amp))
        # print(frequency)
        # return amplitude  # , frequency
        return {'amplitude': amplitude, 'frequency': frequency}

    '''
    inst.write(f':SENS:FREQ:CENT {cf}')
    inst.write(f':SENS:SWE:TIME {(1/rate)*2:.6f}')
    inst.write('INIT:IMM')  # Restart inc AVG
    inst.query('*OPC?')  # is this finished

    xt = np.linspace(0, float(inst.query(':SENS:SWE:TIME?')), int(inst.query(':SENS:SWEEP:POINts?')))
    yt = np.array(inst.query_ascii_values(':TRAC:DATA? TRACE1'))
    '''

    @property
    def frequency(self):
        """Center frequency."""
        return float(self.query(":FREQuency:CENT?"))

    @frequency.setter
    def frequency(self, freq):
        self.write(":FREQuency:CENT {}".format(freq))

    '''
    @property
    def frequency(self):
        return self.query_float(':SENS:FREQ:CENT?')

    @frequency.setter
    def frequency(self, frequency):
        self.write(f':SENS:FREQ:CENT {frequency}')
    '''

    @property
    def sweeppoints(self):
        """Sweep Points."""
        return float(self.query(":SWEep:POINts?"))

    @sweeppoints.setter
    def sweeppoints(self, points):
        # N9030B 1 to 100,001 Zero and non-zero spans
        # E4440A 101 to 8192, 2 to 8192 in zero span
        # [:SENSe]:SWEep:POINts <number of points>
        self.write(":SWEep:POINts {}".format(int(points)))

    @property
    def sweeptime(self):
        """Sweep Time."""
        '''Replace <meas> with the meas name, eg CHPower
        [:SENSe]:<meas>:SWEep:TIME <time>
        [:SENSe]:<meas>:SWEep:TIME?
        [:SENSe]:<meas>:SWEep:TIME:AUTO OFF|ON|0|1
        [:SENSe]:<meas>:SWEep:TIME:AUTO?
        '''
        return float(self.query(":SWEep:TIME?"))

    @sweeptime.setter
    def sweeptime(self, points):
        self.write(":SWEep:TIME {}".format(int(points)))

    @property
    def referenceoutput(self):
        """10MHz output."""
        return bool(self.query(':SENSe:ROSCillator:OUTPUT?'))

    @referenceoutput.setter
    def referenceoutput(self, boolean=True):
        self.write(':SENSe:ROSCillator:OUTPUT:STATe {}'.format(boolean))

    @property
    def referencelevel(self):
        """Reference level."""
        # N9030B Log scale –170 to +30 dBm in 0.01 dB steps
        # N9030B Linear scale 707 pV to 7.07 V with 0.11% (0.01 dB) resolution
        return float(self.query(':DISP:WIND:TRACE:Y:RLEV?'))

    @referencelevel.setter
    def referencelevel(self, lvl):
        self.write(':DISP:WIND:TRACE:Y:RLEV {}'.format(lvl))
        # used for seting reference level to a reasonable amount above the measured value
        # and therefor prevent recording clipped values
        # time.sleep(.2)  # settling time

    @property
    def resolutionbandwidth(self):
        """Resolution Bandwidth."""
        # N9030B 1 Hz to 3 MHz (10% steps), 4, 5, 6, 8 MHz
        # N9030B Bandwidths 1 Hz to 3 MHz are spaced at 10% spacing using
        # the E24 series (24 per decade):
        # 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6,
        # 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1 in each decade
        return self.query(':BANDwidth:RESolution?')

    @resolutionbandwidth.setter
    def resolutionbandwidth(self, resolutionbandwidth, *, unit='Hz'):
        self.write(':BANDwidth:RESolution {} {}'.format(resolutionbandwidth, unit))

    @property
    def videobandwidth(self):
        """Video Bandwidth."""
        # N9030B  1 Hz to 3 MHz (10% steps), 4, 5, 6, 8 MHz
        # N9030B Same as RBW + plus wide-open VBW (labeled 50 MHz)
        return self.query(':BANDwidth:VIDeo?')

    @videobandwidth.setter
    def videobandwidth(self, videobandwidth, *, unit='Hz'):
        self.write(':BANDwidth:VIDeo {} {}'.format(videobandwidth, unit))

    @property
    def unitpower(self):
        """Unit Power.

        DBM|DBMV|DBMA|V|W|A|DBUV|DBUA|DBPW|DBUVM|DBUAM|DBPT|DBG
        """
        self.query(':UNIT:POWer?')
        #  DBM|DBMV|DBMA|V|W|A|DBUV|DBUA|DBPW|DBUVM|DBUAM|DBPT|DBG

    @unitpower.setter
    def unitpower(self, unit):
        self.query(':UNIT:POWer {}'.format(unit))

    @property
    def frequencyspan(self):
        """Frequency Span."""
        return self.query(':FREQuency:SPAN?')

    @frequencyspan.setter
    def frequencyspan(self, span, *, unit='Hz'):
        self.write(':FREQuency:SPAN {} {}'.format(span, unit))

    @property
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

        # self.query(':SENS:BWID:RES?')  # +3.00000000E+006
        # self.query(':SENS:BWID:VID?')  # +5.00000000E+007
        # self.query(':SENS:SWE:TIME?')  # +2.50000000E-002
        # self.query(':DISP:WIND:TRAC:Y:RLEV?')  # -1.000E+01
        # self.query(':DISP:WIND:TRAC:Y:SPAC?')  # LOG.
        # self.query(':DISP:WIND:TRAC:Y:SCAL:PDIV?')  # +1.000E+01
        # self.query(':UNIT:POW?')  # DBM
        # self.query_ascii_values(':TRAC:DATA? TRACE1')  # Values

        self.write('FORM:DATA REAL,32')
        self.write('FORM:BORD SWAP')
        # y = np.array(self.inst.query_binary_values('TRAC:DATA? TRACE1'))
        y = self.query_binary_values('TRAC:DATA? TRACE1', container=np.float64)

        if self.span == 0.0:
            x = np.linspace(0, self.query_float(':SENS:SWE:TIME?'), self.query_int(':SENS:SWEEP:POINts?'))
        else:
            x = np.linspace(self.query_float(':SENS:FREQ:STAR?'), self.query_float(':SENS:FREQ:STOP?'), self.query_int(':SENS:SWEEP:POINts?'))
        return x, y

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


'''
    if SpectrumAnalyser.query(':INSTrument:SELect?') != 'SA':
        SpectrumAnalyser.write(':INSTrument:SELect SA')
        time.sleep(3)  # Loading delay?

    SpectrumAnalyser.write(':SENSe:ROSCillator:OUTPUT:STATe ON')
    SpectrumAnalyser.write(':CALibration:AUTO ALERt')
    SpectrumAnalyser.write(':UNIT:POWer DBM')
    SpectrumAnalyser.frequencyspan = 1e3
    SpectrumAnalyser.resolutionbandwidth = 1e3

'''
'''
 for l in [-20, -25, -30, -35, -40, -45, -50, -55, -60,
          -65, -70, -75, -80, -85, -90, -95, -100, -105, -110, -115, -120, -125, -127]:

    gen.write(f':SOURce:POWer {l} dBm')
    time.sleep(2)

    inst.write('INIT:IMM')
    inst.timeout = 100 * 1000
    inst.query('*OPC?')

    inst.write(f':CALCulate:MARKer{1}:MAX')
    print(f'{float(inst.query(":CALCulate:MARKer1:Y?"))+0.2:.2f}')
    float(inst.query(':SENS:SWE:TIME?'))
for w in [':FORM ASC','*CLS']:
    # print(w)
    inst.write(w)

for q in [
    '*IDN?',
    # '*CAL?',
    ':FORM?',
    ':INST:SEL?',
    # ':SENS:FREQ:STAR?',
    # ':SENS:FREQ:STOP?',
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
    # ':OUTPut:STATe?',

    ':SENS:FREQ:STAR?',
    ':SENS:FREQ:STOP?',
    # ':SENS:FREQ:POINts?',
    ':SENS:FREQ:SPAN?',
]:
    print('{}  :  {}'.format(q, inst.query(q)))
# :SOURce:POWer:TRCKing:PEAK
# :TRACe1|2|3:MODE WRITe|MAXHold|MINHold|VIEW|BLANk

#


*IDN?  :  Agilent Technologies, E4440A,
:FORM?  :  ASC,+8
:INST:SEL?  :  SA
:SENS:BWID:RES?  :  +1.00000000E+004
:SENS:BWID:VID?  :  +1.00000000E+004
:SENS:SWE:TIME?  :  +4.64000000E-003
:UNIT:POW?  :  DBM
:TRACe1:MODE?  :  WRIT
:INITiate:CONTinuous?  :  1
:SYSTem:ERRor:NEXT?  :  +0,"No error"
:SENS:FREQ:STAR?  :  +6.0000000000000000E+009
:SENS:FREQ:STOP?  :  +6.0000000000000000E+009
:SENS:FREQ:SPAN?  :  +0.0000000000000000E+000

'''
'''
*IDN?;
:INST?;
:POW:PRES:USE?;
:INP:PRES:PATH?;
:INP:PRES RF;
*IDN?;
:INST?;
:POW:PRES:USE?;
:INP:PRES:PATH?;
:INP:PRES RF;
:FREQ:START 30MHZ;:FR...
:BAND 120 KHZ;:BAND:V...
*IDN?;
:CORR:OFFS:MAGN 0DB;:...
:CORR:CSET1:DEL;
:CORR:CSET2:DEL;
:CORR:CSET4:DEL;
:CORR:CSET1 ON ;
:CORR:CSET1:DATA 3000...
:CORR:CSET2 ON ;
:CORR:CSET2:DATA 3000...
:CORR:CSET4 OFF ;
:CORR:OFFS:MAGN 0DB;
:POW:PRES:GAIN ON;:PO...
:CALC:LLIN1:DEL;:CALC...
:CALC:LLIN1:DATA 3000...
:CALC:LLIN1:DISP ON;
:EMI:MEAS:DET:QPE ON;...
:CALC:LLIN1:CONT:INT:...
:CALC:LLIN2:CONT:INT:...
UNIT:POW dBuVm;
:CALC:MARK1:PEAK:EXC ...
:FREQ:START 30.000000...
:FREQ:START 300.00000...
:FREQ:CENT 486.000000...
:CALC:MARK1:X  487.00...
:CALC:MARK1:CENT;
:CALC:MARK:MODE POS;
:MEAS:EMI:MARK;*OPC?;
:MEAS:EMI:MARK?;
:FREQ:SPAN 5.000000 MHZ;
:CORR:OFFS:MAGN  10.0...
:POW:PRES:ATT 10.0;
:POW:PRES:ATT 0.0;
:CORR:OFFS:MAGN  0.00...
:CALC:MARK1:MAX:RIGH;
:CALC:MARK1:MAX:RIGH;
:CALC:MARK1:MAX:RIGH;
:CALC:MARK1:MAX:RIGH;
:CALC:MARK1:MAX:NEXT;
:CALC:MARK1:MAX:NEXT;
:FREQ:START 300.00000...
:CALC:MARK1:MAX:NEXT;
:CALC:MARK1:MAX:RIGH;
:CALC:MARK1:MAX:RIGH;
:AVER OFF;
:FREQ:START 30.000000...
:AVER ON;
:AVER OFF;
:TRAC1:MODE WRIT;
:TRAC1:MODE MAXH;
:TRAC1:MODE VIEW;
:TRAC1:MODE BLAN;
:TRAC2:MODE WRIT;
:TRAC3:MODE WRIT;
:TRAC3:MODE MAXH;
:TRAC1:MODE WRIT;
:SENS:EMI:MEAS:DET:DW...
:CORR:OFFS:MAGN 0DB;
:FREQ:START 0.15MHZ;:...
:BAND 9 KHZ;:BAND:VID...
*IDN?;
:CORR:OFFS:MAGN 0DB;:...
:CORR:CSET1:DEL;
:CORR:CSET2:DEL;
:CORR:CSET4:DEL;
:CORR:CSET1 OFF ;
:CORR:CSET2 ON ;
:CORR:CSET2:DATA 1500...
:CORR:CSET4 ON ;
:CORR:CSET4:DATA 1500...
:CORR:OFFS:MAGN -10DB;
:POW:PRES:GAIN OFF;
:CALC:LLIN1:DEL;:CALC...
:CALC:LLIN1:DATA 1500...
:CALC:LLIN1:DISP ON;
:CALC:LLIN2:DATA 1500...
:CALC:LLIN2:DISP ON;
:EMI:MEAS:DET:QPE ON;...
:CALC:LLIN1:CONT:INT:...
:CALC:LLIN2:CONT:INT:...
UNIT:POW dBuV;
:CALC:MARK1:PEAK:EXC ...
:FREQ:START 0.150000M...
:FREQ:START 1.000000M...
:FREQ:START 1.000000M...
:FREQ:START 0.150000M...
:SENS:EMI:MEAS:DET:DW...
:CORR:OFFS:MAGN 0DB;
*IDN?;
:INST?;
:POW:PRES:USE?;
:INP:PRES:PATH?;
:INP:PRES RF;:INP:PRE...
:FREQ:START 1GHZ;:FRE...
:BAND 1 MHZ;:BAND:VID...
*IDN?;
:CORR:OFFS:MAGN 0DB;:...
:CORR:CSET1:DEL;
:CORR:CSET2:DEL;
:CORR:CSET4:DEL;
:CORR:CSET1 ON ;
:CORR:CSET1:DATA 1000...
:CORR:CSET2 ON ;
:CORR:CSET2:DATA 1000...
:CORR:CSET4 ON ;
:CORR:CSET4:DATA 1000...
:CORR:OFFS:MAGN 0DB;
:POW:PRES:GAIN OFF;
:CALC:LLIN1:DEL;:CALC...
:CALC:LLIN1:DATA 1000...
:CALC:LLIN1:DISP ON;
:CALC:LLIN2:DATA 1000...
:CALC:LLIN2:DISP ON;
:EMI:MEAS:DET:QPE OFF...
:CALC:LLIN1:CONT:INT:...
:CALC:LLIN2:CONT:INT:...
UNIT:POW dBuVm;
:CALC:MARK1:PEAK:EXC ...
:BWID  2000.0 kHz;
:BWID  2000.0 kHz;
:BWID  2000.0 kHz;
:BWID  2000.0 kHz;
:AVER OFF;
:AVER ON;
:AVER OFF;
:SENS:EMI:MEAS:DET:DW...
:INP:PRES:PATH?;
:INP:PRES RF;:INP:PRE...
:CORR:OFFS:MAGN 0DB;
:CORR:OFFS:MAGN 0DB;
'''
'''
*IDN?;
:INST:SEL?

:INST?;
:POW:PRES:USE?;
:INP:PRES:PATH?;
:INP:PRES RF;:INP:PRE...
*IDN?;
:INST?;
:POW:PRES:USE?;
:INP:PRES:PATH?;
:INP:PRES RF;:INP:PRE...
:FREQ:START 1GHZ;:FRE...
:BAND 1 MHZ;:BAND:VID...
*IDN?;
:CORR:OFFS:MAGN 0DB;:...
:CORR:CSET1:DEL;
:CORR:CSET2:DEL;
:CORR:CSET4:DEL;
:CORR:CSET1 ON ;
:CORR:CSET1:DATA 1000...
:CORR:CSET2 ON ;
:CORR:CSET2:DATA 1000...
:CORR:CSET4 ON ;
:CORR:CSET4:DATA 1000...
:CORR:OFFS:MAGN 0DB;
:POW:PRES:GAIN OFF;
UNIT:POW dBuVm;
:CALC:LLIN1:DEL;:CALC...
:CALC:LLIN1:DATA 1000...
:CALC:LLIN1:DISP ON;
:CALC:LLIN2:DATA 1000...
:CALC:LLIN2:DISP ON;
:EMI:MEAS:DET:QPE OFF...
:CALC:LLIN1:CONT:INT:...
:CALC:LLIN2:CONT:INT:...
UNIT:POW dBuVm;
:CALC:MARK1:PEAK:EXC ...
:AVER ON;
:AVER OFF;
:INIT:CONT ON;
:INIT:CONT OFF;
:INIT:CONT ON;

ibwrt(UD0, "INIT:IMM;*OPC?", 14 (0xE))
'''
