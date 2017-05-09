#!/usr/bin/env python3
"""Manual Peak hold at a given frequency then sweep predefined span."""

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

# import CIS9942.parse
from pickfile import pickfilesave, pickfileopen
from ETC import ETC
from pandas_helper import dfiteronrows, dflistfrequencyswithin
from immunity import leveler
from filters import stdevlowpass

from IDNs import IDNs
# Instruments
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
formatstr = ['asctime)', 'module)18', 'funcName)12', 'levelname)5', 'message)']
formatstr = '%(' + "s - %(".join(formatstr) + 's'
formatter = logging.Formatter(formatstr)
#  %(name)s

# re.sub(r'[]/\;,><&*:%=+@!#^()|?^', '', logger)
logger = re.sub(r':', '', datetime.now().isoformat() + ".log")  # use regex to fix illegal filename on windows

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

    SignalGenerator = driverdispatcher(pool, Instrument.SignalGenerator.register)
    PowerMeter = driverdispatcher(pool, Instrument.PowerMeter.register)
    SpectrumAnalyser = driverdispatcher(pool, Instrument.SpectrumAnalyser.register)
    WaveformGenerator = driverdispatcher(pool, Instrument.WaveformGenerator.register)
    NetworkAnalyser = driverdispatcher(pool, Instrument.NetworkAnalyser.register)
    ElectronicAttenuator = driverdispatcher(pool, Instrument.ElectronicAttenuator.register)
    DigitalMultimeter = driverdispatcher(pool, Instrument.DigitalMultimeter.register)
    Osciliscope = driverdispatcher(pool, Instrument.Osciliscope.register)

    # alias  IDNs, SignalGenerator, PowerMeter, SpectrumAnalyser, WaveformGenerator, NetworkAnalyser, ElectronicAttenuator, DigitalMultimeter, Osciliscope

    filename = pickfilesave(filetypes=(("Spreadsheet", "*.xlsx"), ))
    wb = Workbook()
    ws = wb.active
    ws.title = input("Sheetname --> ")
    ws.append(["Frequency", "Mean dBm", "stddev", "list dBm"])

    SpectrumAnalyser[0].configure()

    # freq = float("{0:.0f}".format(float(input("Wanted frequency for peaking in GHz: ")) * 1e9))
    freq = float(input("Wanted frequency for peaking in GHz: ")) * 1e9
    print(freq)
    SignalGenerator[0].freq = freq

    SignalGenerator[0].amplimit = 10
    SignalGenerator[0].amp = 10
    SignalGenerator[0].output = True
    SpectrumAnalyser[0].cf = freq

    while input("Manual peak hold, y when ready to sweep --> ") is not "y":
        pass

    EstimatedTime = ETC((18e9-1e9)/100e6)  # CALCulate number of steps in test
    try:
        for freq in np.arange(1e9, 18e9 + 1, 100e6):  # arange is upto but not including max value, thus + 1
            # freq = float("{0:.0f}".format(freq))  # Needed? or units filter @decorator
            print(freq)
            SpectrumAnalyser[0].cf = freq
            SignalGenerator[0].freq = freq

            start = timer()
            time.sleep(1)
            try:
                measurements = stdevlowpass(
                    readback=SpectrumAnalyser[0].measure(freq)[1],
                    tolerance=0.05,
                    delay=0.1,
                    readings=10,
                    abortafter=42)
            finally:
                print(measurements)
                # print(statistics.mean(measurements))
                # print(statistics.stdev(measurements))
                ws.append([freq, statistics.mean(measurements), statistics.stdev(measurements)] + measurements)
                EstimatedTime.append(timer() - start)  # end - start
                print("Estimated time to finish: {} s".format(EstimatedTime.ETC()))
                print()

    finally:
        SignalGenerator[0].output = False
        wb.save(filename + ".xlsx")
