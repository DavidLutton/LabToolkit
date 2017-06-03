#!/usr/bin/env python3
"""SpectrumAnalyser Instrument classes."""
# import time
# import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


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
        return float(self.write(":FREQuency:CENT?"))

    @frequency.setter
    def frequency(self, freq):
        self.write(":FREQuency:CENT {}".format(freq))

    @property
    def sweeppoints(self):
        """Sweep Points."""
        return float(self.write(":SWEep:POINts?"))

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
        return float(self.write(":SWEep:TIME?"))

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


class HPAKSpectrumAnalyser(SpectrumAnalyser):
    """Extra functions for marker functions and configuration."""

    def configure(self):
        """Configure instrument."""
        self.referenceoutput = True
        self.frequencyspan = 1e3
        self.resolutionbandwidth = 1e3
        # self.write(":RBW 1kHz")
        # self.write(":BAND 1kHz")
        # self.write(":FREQuency:SPAN 1KHz")

    @property
    def measurement(self, *, marker=1):
        """Set instrument marker to peak and read X, Y."""
        self.write(":CALCulate:MARKer{}: 1".format(marker))
        self.write(":CALCulate:MARKer{}:MAX".format(marker))

        amplitude = float(self.query(":CALCulate:MARKer1:Y?").strip())  # AMP
        frequency = float(self.query(":CALCulate:MARKer1:X?").strip())  # FREQ

        # return(float(freqmeas), float(amp))
        print(frequency)
        return amplitude  # , frequency


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

        assert self.IDN.startswith('Agilent Technologies, E4440A,')
        # self.query(":SYSTem:OPTions?")
        self.write("*CLS")  # clear error status


class HPE4406A(SpectrumAnalyser):
    """HP E4406A, 7e6 to 4e9.

    .. figure::  images/SpectrumAnalyser/AgilentE4406A.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.freqs = [7e6, 4e9]
        # self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith('Hewlett-Packard,E4406A,')
        self.__preset__()

    # def __repr__(self):
    #    return "{}, {}".format(__name__, self.instrument)
    #    # return "{}, {}".format(__class__, self.instrument)

    # def __preset__(self):

    # self.message("")
    # self.log.info("Get   {} to known state".format(self.instrument.resource_name))
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


class HP8563E(SpectrumAnalyser):
    """HP8563E, 9e3 to 26.5e9.

    .. figure::  images/SpectrumAnalyser/HP8563E.jpg
    """


class HP8564E(SpectrumAnalyser):
    """HP8564E, 9e3 to 40.5e9.

    .. figure::  images/SpectrumAnalyser/HP8564E.jpg
    """


class HP8594E(SpectrumAnalyser):
    """HP8594E, 9e3 to 2.9e9.

    .. figure::  images/SpectrumAnalyser/HP8594E.jpg
    """


class HP8596E(SpectrumAnalyser):
    """HP8596E, 9e3 to 12.8e9.

    .. figure::  images/SpectrumAnalyser/HP8596E.jpg
    """


class HPE4404B(SpectrumAnalyser):
    """HPE4404B, 9e3 to 6.7e9.

    .. figure::  images/SpectrumAnalyser/HPE4404B.jpg
    """


REGISTER = {
    "Hewlett-Packard,E4406A,": HPE4406A,
    "Agilent Technologies, E4440A,": AgilentE4440A,
    # HP 8594E 9e3-40e9
    # HP 8653E -26.5e9


}
