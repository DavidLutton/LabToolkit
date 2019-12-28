#!/usr/bin/env python3

# Standard modules
import logging  # https://docs.python.org/3/library/logging.html
import time  # https://docs.python.org/3/library/time.html
import statistics  # https://docs.python.org/3/library/statistics.html

# Functions or Classes from standard modules
from pprint import pprint  # https://docs.python.org/3/library/pprint.html
from timeit import default_timer as timer  # https://docs.python.org/3/library/timeit.html

# Imports from modules installed by pip
import numpy as np  # https://docs.scipy.org/doc/numpy/reference/routines.html
import pandas as pd  # Python Data Analysis Library http://pandas.pydata.org/
from openpyxl import Workbook  # read/write xlsx/xlsm files https://openpyxl.readthedocs.io/

import labtoolkit as labtk


def stdevlowpass(*, tolerance=0.05, delay=0.1, readings=10, instrument=False, abortafter=42):
    """Standard deviation low pass filter.

    :param tolerance: tolerace upper limit required to pass
    :param delay: delay between readings
    :param readings: readings to take before applying filter
    :param instrument: Instrument that has a measurement function
    :param abortafter: the upper limit before bypassing this filter
    :returns: list of values as made by readback
    """
    try:
        run = 0
        meas = []
        measurethreshold = False
        while measurethreshold is not True:
            run += 1
            if run >= abortafter:
                raise Exception(f"Abort limit reached: {abortafter}")
            meas.append(instrument.measurement)
            # print(meas)
            if len(meas) > readings:
                meas.pop(0)  # remove item at index 0
                stddev = statistics.stdev(meas)
                # print(stddev)
                if stddev < tolerance:
                    measurethreshold = True
            time.sleep(delay)
    finally:
        return(meas)


class ETC(object):
    """Estimated Time to Completion."""

    def __init__(self, numberofpoints):
        """."""
        self.listoftimes = []
        self.points = numberofpoints + 1

    def append(self, timeinseconds, inferprogress=True):
        """Append result of timer."""
        # print(timeinseconds)
        self.listoftimes.append(timeinseconds)
        if inferprogress is True:
            self.points -= 1

    def ETC(self):
        """Estimate Time to Completion."""
        return(f"{statistics.mean(self.listoftimes) * self.points:.2f}")


logging.basicConfig(level=logging.INFO)

with labtk.ResourceManager('') as rm:
    resources = rm.list_resources()
    # resources = ['GPIB1::5::INSTR', 'GPIB1::18::INSTR']
    pprint(resources)
    for ignore in ['ASRL', 'GPIB0::6']:
        resources = [x for x in resources if not x.startswith(ignore)]
    pprint(resources)

    pool = labtk.visaenumerate(rm, resources)
    pprint(pool)
    for a in pool:
        print(f"Discovered {a} ||| {pool[a]}")
        # print(each)
    print(f"Discovered {len(pool)} instruments")
    print("Attaching drivers to recognised instruments")
    pprint(pool)
    instrument = labtk.Instruments()
    pprint(instrument)

    for driver in labtk.driverclasses:
        pod = labtk.driverdispatcher(pool, getattr(labtk, driver).REGISTER)
        if len(pod) != 0:
            setattr(instrument, driver, pod)

    pprint(instrument)

    if instrument.SpectrumAnalyser[0].query(':INSTrument:SELect?') != 'SA':
        instrument.SpectrumAnalyser[0].write(':INSTrument:SELect SA')
        time.sleep(3)  # Loading delay?

    instrument.SpectrumAnalyser[0].write(':SENSe:ROSCillator:OUTPUT:STATe ON')
    instrument.SpectrumAnalyser[0].write(':CALibration:AUTO OFF')
    instrument.SpectrumAnalyser[0].frequencyspan = 1e3
    instrument.SpectrumAnalyser[0].resolutionbandwidth = 1e3

    instrument.SignalGenerator[0].amplimit = 10
    rfpath = input('RF Path (Ref, UUT) : ')
    wb = Workbook()
    ws = wb.active
    # ws.title = input("Sheetname --> ")
    ws.title = rfpath
    ws.append(["Frequency", "Mean dBm", "list dBm"])
    instrument.SignalGenerator[0].amplimit = 0
    instrument.SignalGenerator[0].amplitude = 0
    instrument.SignalGenerator[0].output = True

    EstimatedTime = ETC((18e9 - 1e9) / 100e6)  # CALCulate number of steps in test
    try:
        for frequency in np.arange(1e9, 18e9 + 1, 100e6):  # arange is upto but not including max value, thus + 1
            print(frequency)
            instrument.SpectrumAnalyser[0].frequency = frequency
            instrument.SignalGenerator[0].frequency = frequency

            start = timer()
            time.sleep(1)
            try:
                # SpectrumAnalyser[0].measurement
                measurements = stdevlowpass(
                    instrument=instrument.SpectrumAnalyser[0],
                    tolerance=0.05,
                    delay=0.1,
                    readings=10,
                    abortafter=24)
            finally:
                print(measurements)
                ws.append([frequency, statistics.mean(measurements)] + measurements)
                EstimatedTime.append(timer() - start)  # end - start
                print(f"Estimated time to finish: {EstimatedTime.ETC()} s")
                print()

    finally:
        instrument.SignalGenerator[0].output = False
        wb.save(f'E:/Path-{rfpath}.xlsx')
