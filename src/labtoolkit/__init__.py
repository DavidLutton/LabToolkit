"""."""  #  pylint: disable=logging-fstring-interpolation, pointless-string-statement

import abc
import importlib
import logging
from importlib.metadata import PackageNotFoundError, version
from time import sleep

import pandas as pd

# import numpy as np
import pyvisa

from .drivers import drivers

__version__ = 'unknown package is not installed'
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    pass  # package is not installed


"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.


.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""


# [Logging HOWTO — Python 3 documentation]
# (https://docs.python.org/3/howto/logging.html#library-config)
logger = logging.getLogger(__name__)  # .addHandler(logging.NullHandler())
# logger = logging.getLogger('__main__')

# logger = logging.getLogger()

# logger.info(f'Invoking __init__.py for {__name__}')
# logger.level(0)

# from .Utils.frequency import FrequencyGroup, HarmonicMixer, SourceMultiplier, FrequencySweep
# from .Utils.testrecorder import TestRecorder
# from .Utils.get import get_bytes, get_file, get_latest, get_powerhead_factors, get_testspec
# from .Utils.enumerate import drivers_list, drivers_show, enumerate_instruments
# from .Utils.modulation import Modulation


# class labtoolkit: ...


class Enumerate(metaclass=abc.ABCMeta):
    """."""

    def __init__(self, *, resourcemanager, resources):  # , ignores, additives, appendix):
        """."""
        self.rm = resourcemanager
        self.resources = resources

        self.enumeration = self.enumerate_resources()

        self.driver_map()
        self.driver_load()

        for index, instrument in self.enumeration.iterrows():
            data = self.enumeration.iloc[index].drop(['IDN', 'inst'])
            self.enumeration.iloc[index].inst.description = data.to_dict()

    def df(self):
        """."""
        return self.enumeration

    def select(self, index):
        """."""
        return self.enumeration.iloc[index].inst

    def show(self):
        """."""
        return self.enumeration.drop(['IDN', 'inst'], axis=1)

    def driver_load(self):
        """."""
        targets = self.enumeration.dropna(subset=['Type', 'Driver'])
        # If type or driver missing drop from driver load targets

        for index, instrument in targets.iterrows():
            # print(f"labtoolkit.{instrument.Type}.{instrument.Driver}")

            module = importlib.import_module(f'.{instrument.Type}.{instrument.Driver}', package='labtoolkit')
            # Get the module that contains the driver class

            driver = getattr(module, instrument.Driver)
            # Get the driver class from the module

            self.enumeration.loc[index, 'inst'] = driver(self.rm.open_resource(instrument.Resource))
            # Open the resouce and pass it to the driver

    def enumerate_resources(self):
        """."""
        # resources = self.res.append(additives)

        # resources = [resource for resource in resources if resource not in ignores]

        mapping = pd.DataFrame(columns=['Manufacturer', 'Model', 'Resource', 'IDN', 'Serial', 'inst'])
        for number, resource in enumerate(self.resources):
            # print(f'{number} of {len(resources)-1} : {resource}')
            try:
                logger.info(f'Trying resource {resource}')

                inst = self.rm.open_resource(
                    resource,
                    read_termination='\n',
                    write_termination='\n',
                    timeout=250,
                )
                # mapping.loc[number, 'Resource'] = resource
                IDN = -1
                IDN = inst.query('*IDN?')
                # print(f'{resource} {IDN}')
                # mapping.loc[number, 'IDN raw'] = IDN
                logger.info(f'{resource} {IDN}')
                # if IDN == '+9000002400E+01\r':
                if ',' in IDN:
                    parts = IDN.split(',')
                    parts = [part.strip() for part in parts]  # strip stray whitespace

                    parts[0] = parts[0].title().replace('-', ' ').replace('_', ' ')
                    parts[0] = parts[0].removesuffix('.').removesuffix(' Inc')
                    # HEWLETT-PACKARD,
                    # HEWLETT PACKARD,
                    # Hewlett-Packard,
                    # Hewlett Packard
                    # Normalise to Hewlett Packard

                    if parts[2] == 'ESG-3000A' and parts[3] == 'A.01.00':
                        # Handle out of order IDN from HP ESG-3000A FW A.01.00
                        # Hewlett-Packard, XXnnnnnnnn, ESG-3000A, A.01.00
                        # reorder to match normal IDNs
                        # Hewlett Packard,ESG-3000A,XXnnnnnnnn,A.01.00
                        # This is shown & not explained in HP/Agilent manual
                        parts = [parts[0], parts[2], parts[1], parts[3]]

                    parts[1].removeprefix('MODEL ') if 'MODEL ' in parts[1] else parts[1]
                    # FAO Keithley 7999-6

                    # mapping.loc[number, 'inst'] = inst
                    mapping.loc[number, 'Resource'] = resource
                    mapping.loc[number, 'IDN'] = ', '.join(parts)
                    logger.debug(mapping.loc[number, 'IDN'])
                    mapping.loc[number, 'Manufacturer'] = parts[0]
                    mapping.loc[number, 'Model'] = parts[1]
                    mapping.loc[number, 'Serial'] = parts[2]
                    logger.debug(mapping.loc[number])
                    # mapping.loc[number, 'Type'] = None
                    # mapping.loc[number, 'Driver'] = None
                    #
                if 'ETS Lindgren EMCenter' in IDN:
                    mapping.loc[number, 'Resource'] = resource
                    mapping.loc[number, 'IDN'] = 'ETS Lindgren, EMGen, 0, 0'
                    mapping.loc[number, 'Manufacturer'] = 'ETS Lindgren'
                    mapping.loc[number, 'Model'] = 'EMGen'
                    mapping.loc[number, 'Serial'] = ''

                if ', ' not in IDN and IDN[-1] == '\r':
                    # Found that some old equipment responds with '\r'
                    # When the query is not understood
                    # Retry with 'ID?'

                    logger.error(f'{resource} ...')
                    ID = inst.query('ID?')
                    logger.error(f'{resource} {ID}')
                    if ID == '+0000089012E-01\r':
                        mapping.loc[number, 'Resource'] = resource
                        mapping.loc[number, 'IDN'] = 'Hewlett Packard, 8901B, 0, 0'
                        mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
                        mapping.loc[number, 'Model'] = '8901B'
                        mapping.loc[number, 'Serial'] = ''

                        # mapping.loc[number, 'Serial'] = '0'
                    if ID == 'HP8594E\r':
                        mapping.loc[number, 'Resource'] = resource
                        mapping.loc[number, 'IDN'] = 'Hewlett Packard, 8594E, 0, 0'
                        mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
                        mapping.loc[number, 'Model'] = '8594E'  # 401 pts
                        mapping.loc[number, 'Serial'] = ''

                        # mapping.loc[number, 'Serial'] = '0'

                    if ID == 'HP8593E\r':
                        mapping.loc[number, 'Resource'] = resource
                        mapping.loc[number, 'IDN'] = 'Hewlett Packard, 8593E, 0, 0'
                        mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
                        mapping.loc[number, 'Model'] = '8593E'  # 401 pts
                        mapping.loc[number, 'Serial'] = ''

                        # mapping.loc[number, 'Serial'] = '0'
                if ' NO MESSAGE' in IDN or ' SYNTAX' in IDN:
                    mapping.loc[number, 'Resource'] = resource
                    mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
                    mapping.loc[number, 'Model'] = '8116A'
                    mapping.loc[number, 'Serial'] = ''

            except IndexError:
                pass

            except pyvisa.VisaIOError as error:
                print(error)
                # if e == :
                # VI_ERROR_RSRC_NFOUND
                # VI_ERROR_NLISTENERS
                # VI_ERROR_TMO

                if error.error_code == pyvisa.errors.VI_ERROR_TMO:
                    # If device is active but not answering at all
                    #
                    self.IDN_fallback(inst, resource, mapping, number)

            finally:
                try:
                    # display(mapping)
                    # inst.write('*RST')
                    # inst.write(f'INITiate:CONTinuous {True:b}')  # TODO keep as default ?
                    inst.close()
                except NameError:
                    # Don't raise an error if you cannot close a inst, that probably never opened

                    # NI VISA 20 with Keysight as extra IO reports disconnected end points,
                    # when you don't refresh scan for connected HW
                    # Dosn't necessarily clear then either
                    pass

                # print(f'{resource} {e}')
        return mapping.reset_index(drop=True)

    def IDN_fallback(self, inst, resource, mapping, number):
        funcs = self.IDN_for_NRVS, self.IDN_for_HP, self.IDN_for_HP8903

        # https://stackoverflow.com/a/19523054 handling for loops that could except

        for func in funcs:
            try:
                if func(inst, resource, mapping, number) == True:
                    break
            except pyvisa.VisaIOError as error:
                pass

    def IDN_for_NRVS(self, inst, resource, mapping, number):
        # sleep(.25)
        # inst.write_termination = None
        sleep(0.05)
        inst.write('W5')
        sleep(0.05)
        if inst.query('ZV').startswith('ROHDE & SCHWARZ NRVS'):
            mapping.loc[number, 'Resource'] = resource
            mapping.loc[number, 'Manufacturer'] = 'Rohde Schwarz'
            mapping.loc[number, 'Model'] = 'NRVS'
            mapping.loc[number, 'Serial'] = ''
            return True

    def IDN_for_HP(self, inst, resource, mapping, number):
        ident = inst.query('ID?').strip()
        if ident == 'HP3457A':
            mapping.loc[number, 'Resource'] = resource
            mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
            mapping.loc[number, 'Model'] = ident[2:]
            mapping.loc[number, 'Serial'] = ''
            return True
        if ident[0:2] == 'HP':
            # HP 8563E
            # HP 8564E
            mapping.loc[number, 'Resource'] = resource
            mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
            mapping.loc[number, 'Model'] = ident[2:]
            mapping.loc[number, 'Serial'] = inst.query('SER?').strip()
            return True

    def IDN_for_HP8903(self, inst, resource, mapping, number):
        inst.write_termination = '\n'
        inst.read_termination = '\r\n'

        inst.write('21.1 SP')  # read GPIB address

        if int(float(inst.query('RR'))) == inst.primary_address:
            inst.write('*CL')  # Clear
            # sleep(0.5)
            # print(inst.query('RR'))
            # if float(inst.query('RR')) != inst.primary_address:

            mapping.loc[number, 'Resource'] = resource
            mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
            mapping.loc[number, 'Model'] = '8903B'
            mapping.loc[number, 'Serial'] = ''
            return True

    def driver_map(self):
        """."""
        self.enumeration = pd.merge(drivers, self.enumeration, how='right', on=['Manufacturer', 'Model'])
        for index, inst in self.enumeration.iterrows():
            if pd.isnull(inst['Type']) and pd.isnull(inst['Driver']):
                self.enumeration.loc[index, 'Type'] = 'Unknown'
                self.enumeration.loc[index, 'Driver'] = 'Unknown'

    def drivers_sorted(self):
        """."""
        return drivers.sort_values(['Type', 'Manufacturer', 'Model']).reset_index()[['Type', 'Manufacturer', 'Model', 'Driver']]

    def driver_load_all(self):
        """."""
        for index, value in self.drivers_sorted()[['Type', 'Driver']].drop_duplicates().iterrows():
            # print(f"labtoolkit.{value.Type}.{value.Driver}")
            module = importlib.import_module(f'.{value.Type}.{value.Driver}', package='labtoolkit')
