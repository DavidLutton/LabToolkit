#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from Instrument.GenericInstrument import GenericInstrument as GenericInstrument


class SpectrumAnalyser(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


class KeysightN9030B(SpectrumAnalyser):

    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        self.freqs = [3, 50e9]
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # assert self.IDN.startswith('Agilent Technologies, E4440A,')


class AgilentE4440A(SpectrumAnalyser):
    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        # self.log =logging.getLogger(__name__)
        self.freqs = [3, 26.5e9]
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.freq = 12e9

        assert self.IDN.startswith('Agilent Technologies, E4440A,')
        # self.query(":SYSTem:OPTions?")
        self.write("*CLS")  # clear error status

    def configure(self, setup):
        '''if setup is "Narrow CW Power + 10MHz output enabled":
            print("SETUP")
            self.refout(True)
            # self.write(":RBW 1kHz")
            self.write(":BAND 1kHz")
            self.write(":FREQuency:SPAN 1KHz")  # maybe too narrow if analyser and siggen are not on same ref clock'''
        self.refout(True)
        # self.write(":RBW 1kHz")
        self.write(":BAND 1kHz")
        self.write(":FREQuency:SPAN 1KHz")  # maybe too narrow if analyser and siggen are not on same ref clock

    def cf(self, freq):
        # freq = "{0:.0f}".format(freq)

        if self.freq != freq:  # prevent resubmitting request to set the same frequency
            self.write(":FREQuency:CENT {}".format(freq))
            self.freq = freq
            time.sleep(.3)  # after retuneing wait time for settling

    def measure(self, freq):
        # freq = "{0:.0f}".format(freq)
        self.cf(freq)

        self.write(":CALCulate:MARKer1: 1")
        self.write(":CALCulate:MARKer1:MAX")

        amp = self.query(":CALCulate:MARKer1:Y?").strip()  # AMP
        freqmeas = self.query(":CALCulate:MARKer1:X?").strip()  # FREQ

        return(float(freqmeas), float(amp))

    def reflvl(self, lvl):
        self.instrument.write(":DISP:WIND:TRACE:Y:RLEV " + str(int(lvl)))
        # used for seting reference level to a reasonable amount above the measured value
        # and therefor prevent recording clipped values
        time.sleep(.2)  # settling time

    def refout(self, bool):
        self.query(':SENSe:ROSCillator:OUTPUT?')

        if bool is True:
            self.write(':SENSe:ROSCillator:OUTPUT:STATe 1')
        else:
            self.write(':SENSe:ROSCillator:OUTPUT:STATe 0')


class HPE4406A(SpectrumAnalyser):
    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.freqs = [7e6, 4e9]
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith('Hewlett-Packard,E4406A,')
        self.__preset__()

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __preset__(self):
        # self.message("")
        self.log.info("Get   {} to known state".format(self.instrument.resource_name))
        self.write('RST')


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


register = {
    "Hewlett-Packard,E4406A,": HPE4406A,
    "Agilent Technologies, E4440A,": AgilentE4440A,
    # HP 8594E 9e3-40e9
    # HP 8653E -26.5e9


}
