#!/usr/bin/env python3

from pprint import pprint
from openpyxl import Workbook
import pandas as pd
from timeit import default_timer as timer

# import timeit
import traceback
import sys
import logging
import time
import numpy
import visa
import visa_helper

import gitrevision
import ETA
import CIS9942.parse
import File.file
from pandas_helper import dfiteronrows, dflistfrequencyswithin
from immunity import leveler


import MeasurePwr

# import Instrument.FunctionGenerator
import Instrument.SignalGenerator
# import Instrument.FieldStrength
import Instrument.PowerMeter
# import Instrument.Positioner
# import Instrument.DMM

# visa.log_to_screen()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info('Git revision: ' + gitrevision.git_version())
# log.info('Creating an instance of ' + __name__)

wb = Workbook()
ws = wb.active

ws.append([
    "ffreqset", "ffreqmeas", "fmean", "fstdev",
    "hfreqset", "hfreqmeas", "hmean", "hstdev",
    ])
# rm, pool = visa_helper.enumerate(visa.ResourceManager('@py'))
rm, pool = visa_helper.enumerate(visa.ResourceManager())
#rm, pool = visa_helper.enumerate(visa.ResourceManager('Sim/default.yaml@sim'))

pprint(pool)

generator = visa_helper.driverdispatcher(pool, {
    "HEWLETT-PACKARD,8657A,": Instrument.SignalGenerator.HP8657A,
    "HEWLETT_PACKARD,8664A,": Instrument.SignalGenerator.HP8664A,

    # "Agilent Technologies, E4422B,": Instrument.SignalGenerator.E4422B,
})


PowerMeter = visa_helper.driverdispatcher(pool, {
    # "Agilent Technologies, E4440A,": MeasurePwr.MeasurePwrE4440A,  # For measuring harmonics
    "HEWLETT-PACKARD,437B,": Instrument.PowerMeter.HP437B,
})

PSAPowerMeter = visa_helper.driverdispatcher(pool, {
    "Agilent Technologies, E4440A,": MeasurePwr.MeasurePwrE4440A,  # For measuring harmonics

})

log.info("Discovered " + str(len(generator)) + " SignalGenerators")
log.info("Discovered " + str(len(PowerMeter)) + " PowerMeters")

log.info("Discovered " + str(len(PSAPowerMeter)) + " PowerMeters")

generator[0].amplimit = 10
pprint(generator)
pprint(PowerMeter)
'''PowerMeter[0].correctionfactorinterpolateload(
                                            [100e3, 300e3, 1e6, 3e6, 10e6, 30e6, 50e6, 100e6, 300e6, 1000e6, 2000e6, 3000e6, 4200e6],
                                            [95.1, 97.6, 99.2, 98.8, 98.4, 98.2, 98, 98, 97.9, 97.5, 96.6, 95.1, 90.4]
                                            )
print("Interpolate")
print(PowerMeter[0].correctionfactorinterpolate(2431e6))
'''
# print(generator[each].instrument.query("AP?"))
print(PowerMeter[0].measure())
assert len(generator) >= 1
# assert len(PowerMeter) >= 1

print(dir(generator[0]))
print(generator[0].query("*IDN?"))
print(generator[0].IDN)
'''
Pause off tes
Display table during test - of last ten points # pandas
Display graph during test # matplotlib
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
        '''Actual Stress      6.300
        Forward Power      38.34
        Frequency          1e+09
        Generator Level      1.7
        Target Stress      6.300
        '''

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
