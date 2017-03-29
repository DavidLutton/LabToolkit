#!/usr/bin/env python3

import logging
from pprint import pprint
import pandas as pd
import visa

import visa
import time
import numpy


# from stepsclass import FrequencySweep
# import bus_get

import CIS9942.raw
import CIS9942.parse

# visa.log_to_screen()

rm = visa.ResourceManager()

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# log.info('Instance of FrequencySweep')

df = CIS9942.parse.parse(CIS9942.raw.raw)
with pd.option_context('display.max_rows', 1024):
    pass
    # print(df)



dfCF = pd.read_excel("low band total loss CF.xlsx")
with pd.option_context('display.max_rows', 1024):
    pass
    print(dfCF)
    for item, frame in dfCF.iterrows():
        print(frame["X-Axis (Hz)"])
        print(frame["Total"])


from openpyxl import Workbook
wb = Workbook()
ws = wb.active

'''for item, frame in df.iterrows():
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
'''
