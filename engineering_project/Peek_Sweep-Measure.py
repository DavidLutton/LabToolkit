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
import visa  # [bindings to VISA to control test equipment via GPIB, RS232, IP or USB](https://github.com/hgrecco/pyvisa/)
import numpy as np  # [NumPy](http://www.numpy.org/)
import pandas as pd  # [pandas: Python Data Analysis Library](http://pandas.pydata.org/)
from openpyxl import Workbook  # [Python library to read/write Excel 2010 xlsx/xlsm files](https://openpyxl.readthedocs.io/en/default/)


# --- Import of code of RCI

# import visa_helper
from visa_helper import Instrument, ResourceManager
from visa_helper import driverdispatcher, visaenumerate, visaaddresslist

# import gitrevision

import CIS9942.parse
from File.file import pickfilesave, pickfileopen
from estimatedtime import ETC
from pandas_helper import dfiteronrows, dflistfrequencyswithin
from immunity import leveler

import Instrument.PowerMeter
import Instrument.SignalGenerator
import Instrument.SpectrumAnalyser

# import Instrument.FunctionGenerator
# HP 33120A 15MHz
# Keysight 33500B 20MHz
# HP 8116A 50MHz

# import Instrument.FieldStrength
# EMC-20 # setup & readback DONE
# SI-100
# EMCO 7110

# import Instrument.Positioner
# 2090 H

# import Instrument.DMM
# HP 34401  # readback
# HP 3478A # readback
# Longscale

# import Instrument.NetworkAnalyser
# E8357A
# 4395A

# import Instrument.Osciliscope  # TDS 544A 500e5, DSO5052A 500e6 4GSa/s
# import Instrument.SourceDC  # 6632A 0-20V 0-5A 100W
# import Instrument.SourceAC  # 3001i, 3001iM

__author__ = "David Lutton"
__license__ = "MIT"

# logging.basicConfig(level=logging.INFO)
log = logging.getLogger("RCI")  # Radiated & Conducted Instrumentation
log.setLevel(logging.DEBUG)
formatstr = ['asctime)', 'module)18', 'funcName)12', 'levelname)5', 'message)']
formatstr = '%(' + "s - %(".join(formatstr) + 's'
formatter = logging.Formatter(formatstr)
#  %(name)s

# re.sub(r'[]/\;,><&*:%=+@!#^()|?^', '', logger)
logger = re.sub(r':', '', datetime.now().isoformat() + ".log")  # use regex fix illegal filename

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
log.info('!yet EN 61000-4-6:2014')
log.info('!yet EN 61000-4-3:2006+A1+A2:2010')
log.info("formatstr = {}".format(formatstr))

# log.info('Git revision: ' + gitrevision.git_version()
log.info('Creating a log file in {}'.format(logger))


# with ResourceManager('Sim/default.yaml@sim') as rm:
with ResourceManager('') as rm:
    # 'Sim/default.yaml@sim' '@py', 'ni'

    reso = rm.list_resources()
    # pprint(reso)
    pool = visaenumerate(rm, reso)

    # pool = visaenumerate(rm, visaaddresslist([5, 18], suffix="::INSTR"))
    # pool = visaenumerate(rm, visaaddresslist([13], suffix="::INSTR"))

    for a in pool:
        log.info("Discovered {} ||| {}".format(a, pool[a]))
        # log.info(each)
    log.info("Discovered {} instruments".format(len(pool)))
    log.info("Attaching drivers to recognised instruments")

    SignalGenerator = driverdispatcher(pool, {
        "HEWLETT-PACKARD,8657A,": Instrument.SignalGenerator.HP8657A,
        "HEWLETT_PACKARD,8664A,": Instrument.SignalGenerator.HP8664A,
        "HEWLETT_PACKARD,8665B,": Instrument.SignalGenerator.HP8665B,
        "ANRITSU,MG3691B,": Instrument.SignalGenerator.AnritsuMG3691B,
        "ANRITSU,MG3692A,": Instrument.SignalGenerator.AnritsuMG3692A,
        "ANRITSU,MG3693A,": Instrument.SignalGenerator.AnritsuMG3693A,
        "Agilent Technologies, E4422B,": Instrument.SignalGenerator.AgilentE4422B,
        # Willtron 10e6, 40e9
        '''
        HP 8673M 2-18GHz
        Anritsu MG3710A 100e3, 6e9
        Agilent N5182A 100e3, 6e9
        Marconi 2031 10e3-2.7e9
        Marconi 20nn 10e3-5.4e9
        '''
    })

    PowerMeter = driverdispatcher(pool, {
        "HEWLETT-PACKARD,437B,": Instrument.PowerMeter.HP437B,
        "Agilent Technologies,E4418B,": Instrument.PowerMeter.AgilentE4418B,
        # NVRS
        # R&S ???4
        # Bird 4421
    })

    SpectrumAnalyser = driverdispatcher(pool, {
        "Hewlett-Packard,E4406A,": Instrument.SpectrumAnalyser.HPE4406A,
        "Agilent Technologies, E4440A,": Instrument.SpectrumAnalyser.AgilentE4440A,
        # HP 8594E 9e3-40e9
        # HP 8653E -26.5e9


    })

    log.info("Discovered " + str(len(SignalGenerator)) + " SignalGenerators")
    pprint(SignalGenerator)
    log.info("Discovered " + str(len(PowerMeter)) + " PowerMeters")
    pprint(PowerMeter)
    log.info("Discovered " + str(len(SpectrumAnalyser)) + " SpectrumAnalysers")
    pprint(SpectrumAnalyser)

    filename = pickfilesave(filetypes=(("Spreadsheet", "*.xlsx"), ))
    wb = Workbook()
    ws = wb.active
    sheetname = input("Sheetname --> ")
    ws.title = sheetname
    ws.append(["Frequency", "Mean dBm", "stddev", "list dBm"])
    SpectrumAnalyser[0].setup("Narrow CW Power + 10MHz output enabled")
    freq = "{0:.0f}".format(float(input("Wanted frequency for peaking in GHz: ")) * 1e9)

    SignalGenerator[0].freq(freq)
    SignalGenerator[0].amplimit = 10
    SignalGenerator[0].amp(10)
    SignalGenerator[0].enable()
    SpectrumAnalyser[0].CF(freq)

    while input("Manual peak hold, y when ready to sweep --> ") is not "y":
        pass

    EstimatedTime = ETC((18e9-1e9)/100e6)  # CALCulate number of steps in test

    try:
        for freq in np.arange(1e9, 18e9 + 1, 100e6):  # arange is upto but not including max value, thus + 1
            freq = "{0:.0f}".format(freq)  # Needed? or units filter @decorator
            print(freq)
            SpectrumAnalyser[0].CF(freq)
            SignalGenerator[0].freq(freq)

            start = timer()
            time.sleep(1)

            try:
                measure = False
                meas = []
                delay = 0.1
                stddevtolerance = 0.001
                readings = 10
                while measure is not True:

                    # value = float(PowerMeter[0].query(':FETCh:SCALar:POWer:AC?'))
                    freq, amplitude = SpectrumAnalyser[0].measure(freq)
                    value = amplitude
                    # print(value)
                    meas.append(value)
                    # print(meas)
                    if len(meas) > readings:
                        meas.pop(0)  # remove item at index 0
                        stddev = statistics.stdev(meas)
                        print(stddev)
                        if stddev < stddevtolerance:
                            measure = True
                    time.sleep(delay)
            finally:
                print(meas)
                print(stddev)
                print(statistics.mean(meas))

                ws.append([freq, statistics.mean(meas), stddev] + meas)

                EstimatedTime.append(timer() - start)  # end - start
                print("ETC: {} s".format(EstimatedTime.ETC()))
                print()

    finally:
        generator[0].disable()
        wb.save(filename + ".xlsx")

    '''
    Pause off test
    Display table during test - of last ten points # pandas
    Display graph during test # matplotlib
    '''
