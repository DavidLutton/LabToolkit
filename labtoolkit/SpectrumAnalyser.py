#!/usr/bin/env python3
"""SpectrumAnalyser Instrument classes."""
# import time
# import logging
# from scipy.interpolate import UnivariateSpline
import numpy as np

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class SpectrumAnalyser(GenericInstrument):
    """SpectrumAnalyser SCPI Or Keysight?.

    Overload methods that vary
    """

    # def __init__(self, instrument):
    # pass
    # super().__init__(instrument)

    # def __repr__(self):
    #    return "{}, {}".format(__class__, self.instrument)

    @property
    def frequency(self):
        """Center frequency."""
        return float(self.query(":FREQuency:CENT?"))

    @frequency.setter
    def frequency(self, freq):
        self.write(f":FREQuency:CENT {freq}")

    @property
    def sweeppoints(self):
        """Sweep Points."""
        return float(self.query(":SWEep:POINts?"))

    @sweeppoints.setter
    def sweeppoints(self, points):
        # N9030B 1 to 100,001 Zero and non-zero spans
        # E4440A 101 to 8192, 2 to 8192 in zero span
        # [:SENSe]:SWEep:POINts <number of points>
        self.write(f":SWEep:POINts {int(points)}")

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
        self.write(f":SWEep:TIME {int(points)}")

    @property
    def referenceoutput(self):
        """10MHz output."""
        return bool(self.query(':SENSe:ROSCillator:OUTPUT?'))

    @referenceoutput.setter
    def referenceoutput(self, boolean=True):
        self.write(f':SENSe:ROSCillator:OUTPUT:STATe {boolean}')

    @property
    def referencelevel(self):
        """Reference level."""
        # N9030B Log scale –170 to +30 dBm in 0.01 dB steps
        # N9030B Linear scale 707 pV to 7.07 V with 0.11% (0.01 dB) resolution
        return float(self.query(':DISP:WIND:TRACE:Y:RLEV?'))

    @referencelevel.setter
    def referencelevel(self, lvl):
        self.write(f':DISP:WIND:TRACE:Y:RLEV {lvl}')
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
        self.write(f':BANDwidth:RESolution {resolutionbandwidth} {unit}')

    @property
    def videobandwidth(self):
        """Video Bandwidth."""
        # N9030B  1 Hz to 3 MHz (10% steps), 4, 5, 6, 8 MHz
        # N9030B Same as RBW + plus wide-open VBW (labeled 50 MHz)
        return self.query(':BANDwidth:VIDeo?')

    @videobandwidth.setter
    def videobandwidth(self, videobandwidth, *, unit='Hz'):
        self.write(f':BANDwidth:VIDeo {videobandwidth} {unit}')

    @property
    def unitpower(self):
        """Unit Power.

        DBM|DBMV|DBMA|V|W|A|DBUV|DBUA|DBPW|DBUVM|DBUAM|DBPT|DBG
        """
        self.query(':UNIT:POWer?')
        #  DBM|DBMV|DBMA|V|W|A|DBUV|DBUA|DBPW|DBUVM|DBUAM|DBPT|DBG

    @unitpower.setter
    def unitpower(self, unit):
        self.query(f':UNIT:POWer {unit}')

    @property
    def frequencyspan(self):
        """Frequency Span."""
        return self.query(':FREQuency:SPAN?')

    @frequencyspan.setter
    def frequencyspan(self, span, *, unit='Hz'):
        self.write(f':FREQuency:SPAN {span} {unit}')


class HPAKSpectrumAnalyser(SpectrumAnalyser):
    """Extra functions for marker functions and configuration."""

    def configure(self):
        """Configure engineering_project."""
        self.referenceoutput = True
        self.frequencyspan = 1e3
        self.resolutionbandwidth = 1e3
        # self.write(":RBW 1kHz")
        # self.write(":BAND 1kHz")
        # self.write(":FREQuency:SPAN 1KHz")

    @property
    def measurement(self, *, marker=1):
        """Set instrument marker to peak and read X, Y."""
        # self.write(":CALCulate:MARKer{}: 1".format(marker))
        self.write(f":CALCulate:MARKer{marker}:MAX")

        amplitude = float(self.query(":CALCulate:MARKer1:Y?").strip())  # AMP
        frequency = float(self.query(":CALCulate:MARKer1:X?").strip())  # FREQ

        # return(float(freqmeas), float(amp))
        # print(frequency)
        # return amplitude  # , frequency
        return {'amplitude': amplitude, 'frequency': frequency}

    def trace(self):
        """Get trace."""
        return NotImplemented
        self.write(':FORM ASC')
        self.query(':INST:SEL?')  # SA
        self.query(':SENS:FREQ:STAR?')  # +4.0000000000000000E+010
        self.query(':SENS:FREQ:STOP?')  # +5.0000000000000000E+010
        self.query(':SENS:BWID:RES?')  # +3.00000000E+006
        self.query(':SENS:BWID:VID?')  # +5.00000000E+007
        self.query(':SENS:SWE:TIME?')  # +2.50000000E-002
        self.query(':DISP:WIND:TRAC:Y:RLEV?')  # -1.000E+01
        self.query(':DISP:WIND:TRAC:Y:SPAC?')  # LOG.
        self.query(':DISP:WIND:TRAC:Y:SCAL:PDIV?')  # +1.000E+01
        self.query(':UNIT:POW?')  # DBM
        self.query_ascii_values(':TRAC:DATA? TRACE1')  # Values


class KeysightN9030B(HPAKSpectrumAnalyser):
    """Keysight N9030B, 3 to 50e9.

    .. figure::  images/SpectrumAnalyser/KeysightN9030B.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.freqs = [3, 50e9]
        # self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # assert self.IDN.startswith('Agilent Technologies, E4440A,')


class AgilentE4440A(HPAKSpectrumAnalyser):
    """Agilent E4440A, 3 to 26.5e9.

    .. figure::  images/SpectrumAnalyser/AgilentE4440A.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log =logging.getLogger(__name__)
        self.freqs = [3, 26.5e9]
        # self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        # self.query(":SYSTem:OPTions?")
        # self.write("*CLS")  # clear error status

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")


class HP_E4406A(SpectrumAnalyser):
    """HP E4406A, 7e6 to 4e9.

    .. figure::  images/SpectrumAnalyser/AgilentE4406A.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self._frequency = [7e6, 4e9]

        self.inst = inst
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

        # self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

    # def trace(self):
    #    """Get trace."""
    #    # setup
    #    return self.instrument.query_binary_values(':READ:SPECtrum4?')

    def trace(self):
        """Get trace."""
        return np.array(self.instrument.query_ascii_values(':READ:SPECtrum4?'))

    @property
    def attenuation(self):
        """attenuation."""
        return float(self.query(":SENS:POW:RF:ATT?"))

    @attenuation.setter
    def attenuation(self, freq):
        self.write(f":SENS:POW:RF:ATT {freq}")

    @property
    def span(self):
        """span frequency."""
        return float(self.query(":SENS:SPEC:FREQ:SPAN?"))

    @span.setter
    def span(self, freq):
        self.write(f":SENS:SPEC:FREQ:SPAN {freq}Hz")

    @property
    def axis(self):
        """Return the x axis for current frequency and span."""
        freq = self.frequency
        span = self.span

        return np.linspace(freq - (span / 2), freq + (span / 2), self.points)

    '''

    w(':SENSe:SPECtrum:AVERage:TYPE LOG')
    w(':DISPlay:FORMat:ZOOM')  # :TILE
    w(':DISPlay:SPECtrum:WINDow:TRACe:Y:SCALe:PDIVision 10')
    w(':DISPlay:SPECtrum:WINDow:TRACe:Y:SCALe:RLEVel -20')
    w(':SYSTem:ERRor:VERBose 1')
    q('SYSTem:ERRor?


    '''

    @property
    def frequency(self):
        return float(self.inst.query(':SENSe:FREQuency?'))

    @frequency.setter
    def frequency(self, frequency):
        self.inst.write(f':SENSe:FREQuency {frequency}')

    @property
    def span(self):
        return float(self.inst.query(':SENSe:SPECtrum:FREQuency:SPAN?'))

    @span.setter
    def span(self, frequency):
        self.inst.write(f':SENSe:SPECtrum:FREQuency:SPAN {frequency}')

    @property
    def resbw(self):
        return float(self.inst.query(':SENSe:SPECtrum:BANDwidth:RESolution?'))

    @resbw.setter
    def resbw(self, frequency):
        self.inst.write(f':SENSe:SPECtrum:BANDwidth:RESolution {frequency}')

    def measure_power_at_marker(self):
        timeout = self.inst.timeout
        self.inst.write('INIT:CONT 0')

        self.inst.timeout = 100 * 1000

        self.inst.write('INIT:IMM')  # states init ignored
        # inst.write('INIT:CONT 0')
        self.inst.query('*OPC?')

        # inst.write(f'CALC:SPEC:MARK{1}:MAX')
        # float(inst.query(f'CALC:SPEC:MARK{1}:Y?')), float(inst.query(f'CALC:SPEC:MARK{1}:X?'))
        value = float(self.inst.query(f':CALCulate:SPEC:MARKer{1}:Y?'))
        self.inst.timeout = timeout
        # return float(self.inst.query(f'CALC:SPEC:MARK{1}:Y?'))

        return value

    # def __repr__(self):
    #    return "{}, {}".format(__name__, self.instrument)
    #    # return "{}, {}".format(__class__, self.instrument)

    # def __preset__(self):

    # self.message("")
    # self.log.info("Get   {} to known state".format(self.engineering_project.resource_name))
    # self.write('RST')


'''
inst.timeout = 25000 # http://pyvisa.readthedocs.io/en/stable/resources.html
print(inst.query(":READ:SPECtrum1?"))
print(inst.query(":READ:SPECtrum7?"))
# inst.write('*RST')

":DISPlay:SPECtrum1:WINDow1:TRACe:Y1:PDIVision?"
":DISPlay:SPECtrum1:WINDow1:TRACe:Y1:RLEVel"
":SENSe:SPECtrum:FREQuency:SPAN 10MHZ"
":READ:SPECtrum7"
":READ:SPECtrum4?"
'''


class HP8546A(SpectrumAnalyser):
    """HP8546A, 9e3 to 6.5e9.

    .. figure::  images/SpectrumAnalyser/HP8546A.jpg
    """

    def trace(self):
        """Get trace."""
        return NotImplemented


class HP8563E(SpectrumAnalyser):
    """HP8563E, 9e3 to 26.5e9.

    .. figure::  images/SpectrumAnalyser/HP8563E.jpg
    """

    def trace(self):
        """Get trace."""
        return NotImplemented


class HP8564E(SpectrumAnalyser):
    """HP8564E, 9e3 to 40.5e9.

    .. figure::  images/SpectrumAnalyser/HP8564E.jpg
    """

    def trace(self):
        """Get trace."""
        return NotImplemented


class HP8594E(SpectrumAnalyser):
    """HP8594E, 9e3 to 2.9e9.

    .. figure::  images/SpectrumAnalyser/HP8594E.jpg
    """

    def trace(self):
        """Get trace."""
        return NotImplemented


class HP8596E(SpectrumAnalyser):
    """HP8596E, 9e3 to 12.8e9.

    .. figure::  images/SpectrumAnalyser/HP8596E.jpg
    """

    def trace(self):
        """Get trace."""
        return NotImplemented


class HP_E4404B(HPAKSpectrumAnalyser):
    """HPE4404B, 9e3 to 6.7e9.

    .. figure::  images/SpectrumAnalyser/HPE4404B.jpg
    """

    def trace(self):
        """Get trace."""
        return NotImplemented
        # print(inst.query(':SENS:SWE:TIME?'))
        # xt, yt = np.linspace(0, float(inst.query(':SENS:SWE:TIME?')), int(inst.query(':SENS:SWEEP:POINts?'))), np.array(inst.query_ascii_values(':TRAC:DATA? TRACE1'))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self._frequency = [9e3, 6.7e9]

        self.inst = inst
        # self.inst.timeout = 3000  # Extend the default timeout as it can take a few seconds to get a settled reading
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    '''
    for w in [':FORM ASC', '*CLS']:
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
        print('{}  :  {}'.format(q, inst.query(q)))
    # :SOURce:POWer:TRCKing:PEAK
    # :TRACe1|2|3:MODE WRITe|MAXHold|MINHold|VIEW|BLANk
    '''
    '''
    %%time

    # Pulse modulation test
    # gen set to square, source level

    # SA settings
    span = 0
    # resbw = 10e3
    resbw = 30e3
    trig = '~video, 0dBm'
    points = 8192
    # avg = 20

    cfs = [100e6, 200e6, 385e6, 500e6, 710e6, 745e6, 780e6, 810e6, 870e6, 930e6, 1499e6, 1720e6, 1845e6, 1970e6, 2450e6, 2999e6, 4200e6, 5240e6, 5500e6, 5785e6, 6000e6,]
    rates = [18, 18, 18, 18, 217, 217, 217, 18, 18, 18, 217, 217, 217, 217, 217, 217, 217, 217, 217, 217, 217,]

    # cfs = [ 5785e6, 6000e6,]
    # rates = [ 217, 217, ]

    inst.timeout = 20e3

    #for cf, rate in zip([100e6, 6000e6,], [18, 217,]):
    for cf, rate in zip(cfs, rates):

        gen.write(f':SOUR:FREQ:FIXED {cf}')
        gen.write(f':SOURce:PULM:INTernal:FREQ {rate}')
        inst.write(f':SENS:FREQ:CENT {cf}')
        inst.write(f':SENS:SWE:TIME {(1/rate)*2:.6f}')
        inst.write('INIT:IMM')  # Restart inc AVG
        inst.query('*OPC?')  # is this finished

        xt, yt = np.linspace(0, float(inst.query(':SENS:SWE:TIME?')), int(inst.query(':SENS:SWEEP:POINts?'))), np.array(inst.query_ascii_values(':TRAC:DATA? TRACE1'))

        pulsedepth = yt.max() - np.average(yt, weights=(yt < -40))
        print(f'{cf/1e6}  |  {rate}  |  {pulsedepth:.2f}')
        #  f'{"Time":^9}|{"Temp":^6}|{"Hu":^4}|{"Wind/deg":^10}|{"mm/3hr":^8}|{"Cloud":^7}',


    # inst.query(':INIT:CONT ON')
    '''

    def trace(self):
        """Get trace."""

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
        points = int(self.inst.query(':SENS:SWEEP:POINts?'))
        y = self.inst.query_binary_values('TRAC:DATA? TRACE1', container=np.float64)

        time = False
        frequency = True

        if time:
            x = np.linspace(0, float(self.inst.query(':SENS:SWE:TIME?')), points)
            return x, y
        if frequency:
            x = np.linspace(float(self.inst.query(':SENS:FREQ:STAR?')), float(self.inst.query(':SENS:FREQ:STOP?')), points)
            return x, y

    @property
    def frequency(self):
        return float(self.inst.query(':SENS:FREQ:CENT?'))

    @frequency.setter
    def frequency(self, frequency):
        self.inst.write(f':SENS:FREQ:CENT {frequency}')

    @property
    def span(self):
        return float(self.inst.query(':SENS:FREQ:SPAN?'))

    @span.setter
    def span(self, frequency):
        self.inst.write(f':SENS:FREQ:SPAN {frequency}')

    @property
    def reflevel(self):
        return float(self.inst.query(':DISP:WIND:TRAC:Y:SCAL:RLEV?'))

    @reflevel.setter
    def reflevel(self, level):
        self.inst.write(f':DISP:WIND:TRAC:Y:SCAL:RLEV {level}')


REGISTER = {
    "Hewlett-Packard,E4406A,": HP_E4406A,
    "Agilent Technologies, E4440A,": AgilentE4440A,
    'KeysightN9030B': KeysightN9030B,
    'HP8546A': HP8546A,
    'HP8563E': HP8563E,
    'HP8564E': HP8564E,
    'HP8594E': HP8594E,
    'HP8596E': HP8596E,
    'Hewlett-Packard, E4404B': HP_E4404B,
    # Benchview supported N9040B UXA, N9030A/B PXA, N9020A/B MXA, N9010A/B EXA, N9000A/B CXA, M9290A CXA-m
    # Benchview supported N9320B, N9322C
    # Benchview supported N9342C, N9343C, N9344C
    # Benchview supported E4440A, E4443A, E4445A, E4446A, E4447A, E4448A
    # Benchview supported E4402B, E4404B, E4405B, E4407B
    # Benchview supported E4403B, E4411B, E4408B

}
