#!/usr/bin/env python3
"""Sweep predefined span and measure."""

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

# from IDNs import IDNs
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

    SignalGenerator = driverdispatcher(pool, Instrument.SignalGenerator.REGISTER)
    PowerMeter = driverdispatcher(pool, Instrument.PowerMeter.REGISTER)
    SpectrumAnalyser = driverdispatcher(pool, Instrument.SpectrumAnalyser.REGISTER)
    WaveformGenerator = driverdispatcher(pool, Instrument.WaveformGenerator.REGISTER)
    NetworkAnalyser = driverdispatcher(pool, Instrument.NetworkAnalyser.REGISTER)
    ElectronicAttenuator = driverdispatcher(pool, Instrument.ElectronicAttenuator.REGISTER)
    DigitalMultimeter = driverdispatcher(pool, Instrument.DigitalMultimeter.REGISTER)
    Osciliscope = driverdispatcher(pool, Instrument.Osciliscope.REGISTER)

    # alias  IDNs, SignalGenerator, PowerMeter, SpectrumAnalyser, WaveformGenerator, NetworkAnalyser, ElectronicAttenuator, DigitalMultimeter, Osciliscope
    for each in [SignalGenerator, PowerMeter, SpectrumAnalyser, WaveformGenerator, NetworkAnalyser, ElectronicAttenuator, DigitalMultimeter, Osciliscope]:
        # for each in [WaveformGenerator, ElectronicAttenuator]:
        if len(each) != 0:
            print(each)
            print()
    '''print(ElectronicAttenuator[0].attenuation)
    ElectronicAttenuator[0].attenuation = 10
    print(ElectronicAttenuator[0].attenuation)'''
