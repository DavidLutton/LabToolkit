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
from pandas_helper import dfiteronrows, dflistfrequencyswithin
import File.file


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


'''filetouseforpickCF = File.file.fileopen(
    title="File to filetouseforpickCF",
        filetypes=(("Spreadsheet", "*.xlsx"), ("All files", "*.*"))
    )
'''
filetouseforpickCF = "/home/dalun/Repos/College/Dataset/low band total loss CF.xlsx"
print(filetouseforpickCF)
dfCF = pd.read_excel(filetouseforpickCF)
# print(df)
with pd.option_context('display.max_rows', 1024):
    pass
    print(dfCF)
print()

'''
generate x and y as a list
get a list of freqs in test
and generate a list of its harmionics

interpolate using list of frequencys z against list x of frequencys and list y of correction factors
'''
