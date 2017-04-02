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


class AgilentE4440A(SpectrumAnalyser):
    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        # self.log =logging.getLogger(__name__)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith('Agilent Technologies, E4440A,')
        self.write("*CLS")  # clear error status

    def setup(input):
        if setup = "Narrow CW Power + 10MHz output enabled":
            self.refout(True)
            # self.write(":RBW 1kHz")
            self.write(":BAND 1kHz")
            self.write(":FREQuency:SPAN 1KHz")  # maybe too narrow if analyser and siggen are not on same ref clock

    def cf(freq):
        freq = "{0:.0f}".format(freq)

        if self.freq != freq:  # prevent resubmitting request to set the same frequency
            self.write(":FREQuency:CENT " + freq)
            self.freq = freq
            time.sleep(.3)  # after retuneing wait time for settling

    def measure(self, freq):
        freq = "{0:.0f}".format(freq)
        self.cf(freq)

        self.write(":CALCulate:MARKer1: 1")
        self.write(":CALCulate:MARKer1:MAX")

        amp = self.query(":CALCulate:MARKer1:Y?").strip()  # AMP
        freqmeas = self.query(":CALCulate:MARKer1:X?").strip()  # FREQ

        return(freqmeas, amp)

    def reflvl(self, lvl):
        self.instrument.write(":DISP:WIND:TRACE:Y:RLEV " + str(int(lvl)))
        # used for seting reference level to a reasonable amount above the measured value
        # and therefor prevent recording clipped values
        time.sleep(.2)  # settling time

    def refout(bool):
        self.query(':SENSe:ROSCillator:OUTPUT?')

        if bool is True:
            self.write(':SENSe:ROSCillator:OUTPUT:STATe 1')
        else:
            self.write(':SENSe:ROSCillator:OUTPUT:STATe 0')


class HPE4406A(SpectrumAnalyser):
    def __init__(self, instrument, logger=None):
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
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

inst = rm.open_resource('GPIB0::18::INSTR')
print(inst.query('*IDN?').strip())

inst.timeout = 25000 # http://pyvisa.readthedocs.io/en/stable/resources.html
print(inst.query(":READ:SPECtrum1?"))
print()
print(inst.query(":READ:SPECtrum7?"))

#inst.write('*RST')
time.sleep(1)





#  HP/Agilent E4406A Span Concatenator
":DISPlay:SPECtrum1:WINDow1:TRACe:Y1:PDIVision?"
":DISPlay:SPECtrum1:WINDow1:TRACe:Y1:RLEVel"
":SENSe:SPECtrum:FREQuency:SPAN 10MHZ"
":READ:SPECtrum7"
":READ:SPECtrum4?"



'''
'''    def discover(self):
        decodeTHISARRAY = self.query("LP2")  # TODO

    def measure(self):
        measure = float(self.query("?"))
        if measure is not 9e40 and measure is not 9.0036e40:
            return(measure)

    def message(self, message=None):
        if message is not None and len(message) <= 12:
            self.write("DU" + message.rjust(12))
        else:
            self.write("DE")

    def displayread(self):
        pass  # OD

    def key(self, key):
        dispatch = {
            "Up": "UP",  # Up arrow key
            "Down": "DN",  # Down arrow key
            "Left": "LT",  # Left arrow key
            "Right": "RT",  # Right arrow key
            "Enter": "EN",  # Enter key
            "Exit": "EX",  # exit function
            "Preset": "PR",
            "Special": "SP",
            "Zero": "ZE",
        }
        # print(dispatch[key])  # PowerMeter[0].key("Left")
        self.write(dispatch[key])

    # def display(self, key):
    # print(dispatch[key])  # PowerMeter[0].key("Left")
    # self.instrument.write(dispatch[key])

    def zero(self):
        self.write("CS;ZE")

    def calibrate(self, factor=100.0):
        self.write("CS;CL{}EN".format(factor))

    def correctionfactor(self, factor=100.0):
        self.write("KB{}EN".format(factor))  # KB enter measurement cal factor

    def statusmessage(self):
        status = self.query("SM")
        #  $Message[5,6] = “06” Wait until zero completes (06 means zeroing)
        #  $Message[5,6] = ! Wait until cal completes (08 means calibrating
        return(status)

    def rangeauto(self):
        self.write("RA")

    def rangehold(self):  # RH Range hold
        self.write("RH")

    def rangemanual(self, range):
        self.write("RM")

    def lin(self):  # Linear units (Watts/%)
        self.write("LN")
        self.units = "W"

    def unitslog(self):  # Log units dBM/dB
        self.write("LG")
        self.units = "dBm"

'''
