import io
import re
from functools import lru_cache
from pathlib import Path, PurePath

import pandas as pd
# import numpy as np
from scipy import interpolate


def get_testspec(spec, sheet_name):
    """."""
    df = pd.read_excel(spec, sheet_name=sheet_name).dropna(how='all')

    try:
        df = df[df['Enabled'] is True]  # filter for Enabled
        df = df.drop(columns=['Enabled'])
    except KeyError:
        pass

    # Normalize frequencies to Hz
    SI_PREFIXES = 'yzafpnum kMGTPEZY'
    SI_SCALE_FACTOR = dict([(key, 10**((-8 + i) * 3)) for i, key in enumerate(SI_PREFIXES)])

    for column in df:
        xHz = [r for r in re.split(r'[\(*\)]', column) if r not in ''][-1]
        # find eg 'MHz' from the column name 'Frequency (MHz)'

        if xHz[-2:] == 'Hz' and len(xHz) == 3:  # check is both ends 'Hz' and has length to be a prefix
            to = column[:-5] + '(Hz)'  # get column label without (?Hz) and append '(Hz)'
            df = df.rename(columns={column: to})  # rename

            df[to] = SI_SCALE_FACTOR[xHz[0]] * df[to]  # scale to Hz

            # consider rounding to ~ 8 decimal places to cut off multiplication errors

    return df


def get_powerhead_factors(spec):
    """."""
    factors = get_testspec(spec, 'Factors')[['Frequency (Hz)', 'Calibration Factor (%)']]
    inter = interpolate.interp1d(factors['Frequency (Hz)'], factors['Calibration Factor (%)'])
    return inter


def get_bytes(file):
    return io.BytesIO(file.read_bytes())


def get_file(file):
    cached_get_bytes = lru_cache(maxsize=32)(get_bytes)
    if isinstance(file, PurePath):  # https://stackoverflow.com/questions/58647584/how-to-test-if-object-is-a-pathlib-path
        return cached_get_bytes(file)


def get_latest(parent, glob):
    """Return last file from a glob of files."""
    # where ISO 8601 format date 2000-12-14
    # where Config v0,1,...,9,10,11
    # last == latest file

    # glob like 'Config SwitchPaths v*.xlsx'
    if parent is None:
        parent = Path.cwd()
    return sorted(list(parent.glob(glob)))[-1]
