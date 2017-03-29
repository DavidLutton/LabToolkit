#!/usr/bin/env python3

import logging
from pprint import pprint
import pandas as pd
import visa

import visa
import time
import numpy


# from stepsclass import FrequencySweep
import bus_get

import CIS9942.raw
import CIS9942.parse

# visa.log_to_screen()


rm = visa.ResourceManager()

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# log.info('Instance of FrequencySweep')

E4440A = rm.open_resource('GPIB0::18::INSTR')
assert E4440A.query('*IDN?').startswith('Agilent Technologies, E4440A')

E4440A.write("*CLS")  # clear error status
#  ? E4440A.write(":RBW 1kHz") 
E4440A.write(":BAND 1kHz") 
E4440A.write(":FREQuency:SPAN 1KHz")


generator = rm.open_resource('GPIB0::19::INSTR')
assert generator.query('*IDN?').startswith('Agilent Technologies, ')

generator.write("OUTP:STAT ON")

df = CIS9942.parse.parse(CIS9942.raw.raw)
with pd.option_context('display.max_rows', 1024):
    pass
    # print(df)

from openpyxl import Workbook
wb = Workbook()
ws = wb.active

class MeasurePwr:

    def __init__(self, E4440A):
        self.E4440A = E4440A
        self.freq = ""

    def measure(self, freq):
        freq = "{0:.0f}".format(freq)
        
        if self.freq != freq:
            self.E4440A.write(":FREQuency:CENT " + freq)
            self.freq = freq
            time.sleep(.3)
        
        self.E4440A.write(":CALCulate:MARKer1: 1")
        self.E4440A.write(":CALCulate:MARKer1:MAX")

        amp  = self.E4440A.query(":CALCulate:MARKer1:Y?").strip()  # AMP
        freqmeas = self.E4440A.query(":CALCulate:MARKer1:X?").strip()  # FREQ

        return(freqmeas, amp)
    def reflvl(self, lvl):
        self.E4440A.write(":DISP:WIND:TRACE:Y:RLEV " + str(int(lvl)))
        time.sleep(.2)

PSA = MeasurePwr(E4440A)
genlevel = -60

for item, frame in df.iterrows():
    # print(item)
    # print(frame)
    freq, gen, pwr = frame
    print(freq)
    print(gen)
    print(pwr)

    genlevel = -10
    generator.write("POW:AMPL " + str(genlevel) + " dBm")
    time.sleep(0.2)
    generator.write("FREQ " + str(freq) + " Hz")
    time.sleep(0.2)
    genlevel = gen
    generator.write("POW:AMPL " + str(genlevel) + " dBm")
    freqmeas, amp = PSA.measure(freq)
    
    time.sleep(1)
    
    measurements = []
    measurementfreq = []

    freqmeas, amp = PSA.measure(freq)
    PSA.reflvl(float(amp) + 10)

    for reads in range(5):
        time.sleep(.1)
        freqmeas, amp = PSA.measure(freq)
        
        # measurements[reads] = {float(freq): float(amp)}
        measurements.append(float(amp))
        measurementfreq.append(float(freqmeas))
    # pprint(measurements)

    result = {
        "freqset"  : freq,
        "freqmeas" : numpy.mean(measurementfreq),
        "mean" :  numpy.mean(measurements),
        "stdev" : numpy.std(measurements),
    }
    pprint(result)
    with open("testfund" + ".csv", "a") as file:
        file.write(
            str(result["freqset"]) + ", " +
            str(result["freqmeas"]) + ", " +
            str(result["mean"]) + ", " +
            str(result["stdev"]) + "\n")
    print("")
    fundementalresult = result
    
    measurements = []
    measurementfreq = []
    meas = float(freqmeas) * 3
    for reads in range(5):
        time.sleep(.1)
        freqmeas, amp = PSA.measure(meas)

        # measurements[reads] = {float(freq): float(amp)}
        measurements.append(float(amp))
        measurementfreq.append(float(freqmeas))
    # pprint(measurements)

    result = {
        "freqset"  : freq,
        "freqmeas" : numpy.mean(measurementfreq),
        "mean" :  numpy.mean(measurements),
        "stdev" : numpy.std(measurements),
    }
    pprint(result)
    harmonicresult = result
    
    with open("testharm" + ".csv", "a") as file:
        file.write(
            str(result["freqset"]) + ", " +
            str(result["freqmeas"]) + ", " +
            str(result["mean"]) + ", " +
            str(result["stdev"]) + "\n")
    print("")

    ws.append([
        fundementalresult["freqset"],
        fundementalresult["freqmeas"],
        fundementalresult["mean"],
        fundementalresult["stdev"],
        harmonicresult["freqset"],
        harmonicresult["freqmeas"],
        harmonicresult["mean"],
        harmonicresult["stdev"]
        ])
generator.write("OUTP:STAT OFF")

wb.save("test" + ".xlsx")
