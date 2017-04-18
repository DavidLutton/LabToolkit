#!/usr/bin/env python3

# Standard modules
import traceback
import sys
import logging
import time
import re
import statistics

# Functions from standard modules
from pprint import pprint
from timeit import default_timer as timer
from datetime import datetime


# Imports from modules installed by pip
import visa  # [bindings to the "Virtual Instrument Software Architecture" in order to control measurement devices and test equipment via GPIB, RS232, or USB.](https://github.com/hgrecco/pyvisa/)
import numpy as np  # [NumPy](http://www.numpy.org/)
import pandas as pd  # [pandas: Python Data Analysis Library](http://pandas.pydata.org/)
from openpyxl import Workbook  # [openpyxl - A Python library to read/write Excel 2010 xlsx/xlsm files — openpyxl documentation](https://openpyxl.readthedocs.io/en/default/)


# --- Import of code of RCI

# import visa_helper
from visa_helper import Instrument, ResourceManager
from visa_helper import driverdispatcher, visaenumerate, visaaddresslist

# import gitrevision

import CIS9942.parse
from pickfile import pickfilesave, pickfileopen
from estimatedtime import ETC
from pandas_helper import dfiteronrows, dflistfrequencyswithin
from immunity import leveler
from filters import stdevlowpass

# stdevlowpass(readback=0,)


import Instrument.PowerMeter
import Instrument.SignalGenerator
import Instrument.WaveformGenerator
import Instrument.SpectrumAnalyser
import Instrument.NetworkAnalyser
import Instrument.ElectronicAttenuator
import Instrument.DigitalMultimeter
import Instrument.EnviromentalChamber
import Instrument.Osciliscope
import Instrument.FieldStrength
import Instrument.Positioner  # 2090 H
import Instrument.SourceDC  # 6632A 0-20V 0-5A 100W
import Instrument.SourceAC  # 3001i, 3001iM


__author__ = "David Lutton"
__license__ = "MIT"

# logging.basicConfig(level=logging.INFO)
log = logging.getLogger("RCI")  # Radiated & Conducted Instrumentation
log.setLevel(logging.DEBUG)
formatstr = ['asctime)', 'module)18', 'funcName)12', 'levelname)', 'message)']
formatstr = '%(' + "s - %(".join(formatstr) + 's'
formatter = logging.Formatter(formatstr)
#  %(name)s

logger = datetime.now().isoformat() + ".log"
# re.sub(r'[]/\;,><&*:%=+@!#^()|?^', '', logger)
logger = re.sub(r':', '', logger)
# print(logger)
# python3.6 isoformat(timespec='seconds')

fh = logging.FileHandler(logger)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)


log.addHandler(fh)
log.addHandler(ch)


# visa.log_to_screen()
log.info("Starting Radiated & Conducted Instrumentation")
log.info("Software by {}".format(__author__))
log.info('! EN 61000-4-6:2014')
log.info('! EN 61000-4-3:2006+A1+A2:2010')
log.info("formatstr = {}".format(formatstr))

# log.info('Git revision: ' + gitrevision.git_version()
log.info('Creating a log file in {}'.format(logger))

wb = Workbook()
ws = wb.active

# with ResourceManager('Sim/default.yaml@sim') as rm:
with ResourceManager('') as rm:
    # 'Sim/default.yaml@sim' '@py', 'ni'

    reso = rm.list_resources()
    pprint(reso)
    pool = visaenumerate(rm, reso)

    # pool = visaenumerate(rm, visaaddresslist([5, 18], suffix="::INSTR"))
    # pool = visaenumerate(rm, visaaddresslist([13], suffix="::INSTR"))
    pprint(pool)
    for each in pool:
        log.info("Discovered {}".format(each))
        # log.info(each)
    log.info("Discovered {} instruments".format(len(pool)))
    log.info("Attaching drivers to recognised instruments")

    SignalGenerator = driverdispatcher(pool, Instrument.SignalGenerator.register)
    PowerMeter = driverdispatcher(pool, Instrument.PowerMeter.register)
    SpectrumAnalyser = driverdispatcher(pool, Instrument.SpectrumAnalyser.register)
    WaveformGenerator = driverdispatcher(pool, Instrument.WaveformGenerator.register)
    NetworkAnalyser = driverdispatcher(pool, Instrument.NetworkAnalyser.register)
    ElectronicAttenuator = driverdispatcher(pool, Instrument.ElectronicAttenuator.register)
    DigitalMultimeter = driverdispatcher(pool, Instrument.DigitalMultimeter.register)
    EnviromentalChamber = driverdispatcher(pool, Instrument.EnviromentalChamber.register)
    Osciliscope = driverdispatcher(pool, Instrument.Osciliscope.register)

    log.info("Discovered " + str(len(generator)) + " SignalGenerators")
    pprint(generator)
    log.info("Discovered " + str(len(PowerMeter)) + " PowerMeters")
    pprint(PowerMeter)
    log.info("Discovered " + str(len(SpectrumAnalyser)) + " SpectrumAnalysers")
    pprint(SpectrumAnalyser)

    ws.append([
        "ffreqset", "ffreqmeas", "fmean", "fstdev",
        "hfreqset", "hfreqmeas", "hmean", "hstdev",
        "Generator level dBm"
        ])
    # generator[0].amplimit = 10

    '''PowerMeter[0].correctionfactorinterpolateload(
                                                [100e3, 300e3, 1e6, 3e6, 10e6, 30e6, 50e6, 100e6, 300e6, 1000e6, 2000e6, 3000e6, 4200e6],
                                                [95.1, 97.6, 99.2, 98.8, 98.4, 98.2, 98, 98, 97.9, 97.5, 96.6, 95.1, 90.4]
                                                )
    print("Interpolate")
    print(PowerMeter[0].correctionfactorinterpolate(2431e6))
    '''
    # SpectrumAnalyser[0].setup("Narrow CW Power + 10MHz output enabled")
    freq = "{0:.0f}".format(float(input("Wanted frequency GHz: ")) * 1e9)
    # SignalGenerator[0].freq(freq)
    # SpectrumAnalyser[0].CF(freq)

    while input("Manual peek hold, y when ready to sweep") is not "y":
        pass

    for freq in np.arange(1e9, 18e9 + 1, 100e6):
        freq = "{0:.0f}".format(freq)
        print(freq)
        # SignalGenerator[0].freq(freq)
        # SpectrumAnalyser[0].CF(freq)

    '''try:
        measure = False
        meas = []
        delay = 0.1
        stddevtolerance = 0.001
        readings = 10
        while measure is not True:
            value = float(PowerMeter[0].query(':FETCh:SCALar:POWer:AC?'))
            # print(value)
            meas.append(value)
            # print(meas)
            if len(meas) > readings:
                meas.pop(0)  # remove item at index 0
                stddev = statistics.stdev(meas)
                # print(stddev)
                if stddev < stddevtolerance:
                    measure = True
            time.sleep(delay)
    finally:
        print(meas)
        print(stddev)
        print(statistics.mean(meas))
    '''
    # print(generator[each].instrument.query("AP?"))
    # print(PowerMeter[0].measure())
    # assert len(generator) >= 1
    # assert len(PowerMeter) >= 1

    # print(dir(generator[0]))
    # print(generator[0].query("*IDN?"))
    # print(generator[0].IDN)

    '''
    Pause off tes
    Display table during test - of last ten points # pandas
    Display graph during test # matplotlib
    '''
    '''
    filetorunharmonicscheckagainst = File.file.fileopen(title="File to run harmonics check against", filetypes=(("CAL files", "*.CAL;*.cal"), ("All files", "*.*")))
    # filetorunharmonicscheckagainst = "Dataset/20170113-K/CALS/140115V7.CAL"
    print(filetorunharmonicscheckagainst)

    with open(filetorunharmonicscheckagainst, 'r') as f:
        df = CIS9942.parse.parse(f.readlines())
        # print(df)
        with pd.option_context('display.max_rows', 1024):
            pass
            # print(df)
        print()
        print()

    # for step in dfiteronrows(df):
        # print(step['Frequency'])
        # print(step)

    # print(dflistfrequencyswithin(df))

    rowsource = dfiteronrows(df)

    EstimatedTime = ETA.estimatedtime(len(df))
    # EstimatedTime.append(10)
    # EstimatedTime.append(19)

    try:
        generator[0].start()

        for row, index in rowsource:
            start = timer()
            print()
            print()
            print(row)
            print()
            print(index)

            print(index)
            print(row)

            # time.sleep(1)

            freq = row['Frequency']
            print()
            print(row['Generator Level'])

            generator[0].freq(row['Frequency'])

            # freqmeas, amp = PowerMeter.measure(freq)
            # couplingoffsetfromCISsetup = ((-0.0000000024 * int(freq)) + 40.4)
            # couplingoffsetfromCISsetup = 30
            # couplingdelta = couplingoffsetfromCISsetup - couplingoffsetfromdirectmeasurements

            # couplingoffset = couplingdelta + couplingoffsetfromCISsetup
            # expectedpower = float(row["Forward Power"]) - couplingoffset
            # print(round(expectedpower, ndigits=2))

            measure = False

            while measure is not True:
                errorpwr, errorcent, newlevel = leveler(
                        PowerMeter[0].measure(),
                        float(row['Forward Power'])-50.0,
                        generator[0].amplitude,
                )
                print(newlevel)
                generator[0].ampsetter(newlevel)
                print("Error Power " + str(errorpwr))
                if 0.1 >= errorpwr >= -0.1:
                    measure = True
                    ###### generator[0].lvl
                    time.sleep(1)  # Settling time

                    measurements = []
                    measurementfreq = []

                    freqmeas, amp = PSAPowerMeter[0].measure(freq)
                    PSAPowerMeter[0].reflvl(float(amp) + 10)

                    for reads in range(5):
                        time.sleep(.1)
                        freqmeas, amp = PSAPowerMeter[0].measure(freq)

                        # measurements[reads] = {float(freq): float(amp)}
                        measurements.append(float(amp))
                        measurementfreq.append(float(freqmeas))
                    # pprint(measurements)

                    result = {
                        "freqset": freq,
                        "freqmeas": numpy.mean(measurementfreq),
                        "mean":  numpy.mean(measurements),
                        "stdev": numpy.std(measurements),
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
                        freqmeas, amp = PSAPowerMeter[0].measure(meas)

                        # measurements[reads] = {float(freq): float(amp)}
                        measurements.append(float(amp))
                        measurementfreq.append(float(freqmeas))
                    # pprint(measurements)

                    result = {
                        "freqset": freq,
                        "freqmeas": numpy.mean(measurementfreq),
                        "mean":  numpy.mean(measurements),
                        "stdev": numpy.std(measurements),
                    }
                    pprint(result)
                    harmonicresult = result

                    with open("testharm" + ".csv", "a") as file:
                        file.write(
                            str(result["freqset"]) + ", " +
                            str(result["freqmeas"]) + ", " +
                            str(result["mean"]) + ", " +
                            str(result["stdev"]) + "\n")
                    print()

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

            EstimatedTime.append(timer() - start)  # end - start
            print("ETA: " + str(EstimatedTime.ETA()) + " s")
            print()

    finally:
        generator[0].safe()
        generator[0].disable()
        wb.save("test" + ".xlsx")
    '''
