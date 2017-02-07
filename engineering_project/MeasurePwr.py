#!/usr/bin/env python3
import logging
import time

class MeasurePwrE4440A:

    def __init__(self, E4440A):
        self.instrument = E4440A
        self.log = logging.getLogger(__name__)
        self.log.info('Creating an instance of ' + str(__class__))
        self.log.info('Instrument path\t' + str(self.instrument))
        self.IDN = self.instrument.query('*IDN?')
        self.log.info('Instrument IDN\t' + self.IDN)

        assert self.IDN.startswith('Agilent Technologies, E4440A')
        self.freq = ""  # used to track what freq set to analyser
        self.instrument.write("*CLS")  # clear error status
        # self.E4440A.write(":RBW 1kHz")
        self.instrument.write(":BAND 1kHz")
        self.instrument.write(":FREQuency:SPAN 1KHz")  # maybe too narrow if analyser and siggen are not on same ref clock

    def measure(self, freq):
        freq = "{0:.0f}".format(freq)

        if self.freq != freq:  # prevent resubmitting request to set the same frequency
            self.instrument.write(":FREQuency:CENT " + freq)
            self.freq = freq
            time.sleep(.3)  # after retuneing wait time for settling

        self.instrument.write(":CALCulate:MARKer1: 1")
        self.instrument.write(":CALCulate:MARKer1:MAX")

        amp = self.instrument.query(":CALCulate:MARKer1:Y?").strip()  # AMP
        freqmeas = self.instrument.query(":CALCulate:MARKer1:X?").strip()  # FREQ

        return(freqmeas, amp)

    def reflvl(self, lvl):
        self.instrument.write(":DISP:WIND:TRACE:Y:RLEV " + str(int(lvl)))
        # used for seting reference level to a reasonable amount above the measured value
        # and therefor prevent recording clipped values
        time.sleep(.2)  # settling time
