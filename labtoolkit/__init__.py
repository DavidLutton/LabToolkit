""".""" #  pylint: disable=logging-fstring-interpolation, pointless-string-statement
import abc
import importlib
import logging
from time import sleep

import pandas as pd
# import numpy as np
import pyvisa

"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.


.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""



# [Logging HOWTO — Python 3 documentation]
# (https://docs.python.org/3/howto/logging.html#library-config)
logger = logging.getLogger(__name__) # .addHandler(logging.NullHandler())
# logger = logging.getLogger('__main__')

# logger = logging.getLogger()

# logger.info(f'Invoking __init__.py for {__name__}')
# logger.level(0)

# from .Utils.frequency import FrequencyGroup, HarmonicMixer, SourceMultiplier, FrequencySweep
# from .Utils.testrecorder import TestRecorder
# from .Utils.get import get_bytes, get_file, get_latest, get_powerhead_factors, get_testspec
# from .Utils.enumerate import drivers_list, drivers_show, enumerate_instruments
# from .Utils.modulation import Modulation


class Enumerate(metaclass=abc.ABCMeta):

    """."""

    def __init__(self, *, resourcemanager, resources): # , ignores, additives, appendix):
        """."""
        self.rm = resourcemanager
        self.resources = resources


        self.enumeration = self.enumerate_resources()

        
        # add resources in appendix to ignore (for enumerate_resources list)

        # if not appendix.empty:
        #  ignores = [resource for resource in res*** if resource in list(appendix['Resource'])]
        #if additives is not None:
        #    self.enumeration = self.enumerate_resources(ignores, additives)
        #else:
        #    self.enumeration = self.enumerate_resources(ignores, additives=[])

        # interject insts that don't respond to *IDN?
        #if not appendix.empty:
        #    self.enumeration = pd.concat(
        #        [self.enumeration, appendix],
        #        axis=0,
        #        join='outer',
        #        ignore_index=True
        #    )

        self.driver_map()
        # display(self.enumeration)
        self.driver_load()

        self.__post__()
        # return self.enumeration

    def __post__(self):
        """."""
        pass

    def df(self):
        return self.enumeration
    
    def show(self):
        return self.enumeration.drop([
            'IDN', 'inst'
            ], axis=1)

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

        mapping = pd.DataFrame(columns=['Manufacturer', 'Model'])
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
                IDN = inst.query("*IDN?")
                # print(f'{resource} {IDN}')
                # mapping.loc[number, 'IDN raw'] = IDN
                logger.info(f'{resource} {IDN}')
                # if IDN == '+9000002400E+01\r':
                if ',' in IDN:
                    parts = IDN.split(',')
                    parts = [part.strip() for part in parts]  # strip stray whitespace

                    parts[0] = parts[0].title().replace('-', ' ').replace('_', ' ')
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
                        # This is show & not explained in HP/Agilent manual
                        parts = [parts[0], parts[2], parts[1], parts[3]]

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
        funcs = self.IDN_for_NVRS, self.IDN_for_HP8563E
        
        # https://stackoverflow.com/a/19523054 handling for loops that could except
        
        for func in funcs:
            try:
                if func(inst, resource, mapping, number) == True:
                    break
            except pyvisa.VisaIOError as error:
                pass

    def IDN_for_NVRS(self, inst, resource, mapping, number):
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

    def IDN_for_HP8563E(self, inst, resource, mapping, number):
        if inst.query('ID?').strip() == 'HP8563E':
            mapping.loc[number, 'Resource'] = resource
            mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
            mapping.loc[number, 'Model'] = '8563E'  # 601 pts
            mapping.loc[number, 'Serial'] = inst.query('SER?').strip()
            return True

    drivers = pd.DataFrame([
        ['Marconi Instruments', '2187', 'Attenuator', 'MI2187'],
        ['MI Wave', '511', 'Attenuator', 'MIWave5nn'],

        ['Hewlett Packard', '8903B', 'AudioAnalyser', 'HP8903B'],

        ['Hewlett Packard', '34401A', 'DigitalMultimeter', 'HP34401A'],
        ['Hewlett Packard', '3457A', 'DigitalMultimeter', 'HP3457A'],

        ['Lumiloop', 'LSProbe', 'FieldStrength', 'LumiloopLSProbe'],
        ['Wandel Goltermann', 'EMC20', 'FieldStrength', 'WandelGoltermannEMC20'],

        ['Agilent Technologies', 'N9039A', 'FilterRF', 'AgilentN9039A'],

        ['Hewlett Packard', '53132A', 'FrequencyCounter', 'HP53132A'],
        ['Racal', '1992', 'FrequencyCounter', 'Racal1992'],

        ['Hewlett Packard', '8901B', 'ModulationMeter', 'HP8901B'],
        ['Marconi Instuments', '2305', 'ModulationMeter', 'MI2305'],

        ['Hewlett Packard', '4395A', 'NetworkAnalyser', 'HP4395A'],
        ['Agilent Technologies', 'E8357A', 'NetworkAnalyser', 'AgilentE8357A'],
        ['Anritsu', 'MS46122B', 'NetworkAnalyser', 'AnritsuShockline'],
        ['Wiltron', '360', 'NetworkAnalyser', 'Wiltron360'],

        ['Keysight Technologies', 'DSO-X 3034T', 'Oscilloscope', 'KeysightInfiniiVisionX'],
        ['Agilent Technologies', 'DSO5052A', 'Oscilloscope', 'KeysightInfiniiVisionX'],  # KeysightDSO50bpA
        ['Agilent Technologies', 'DSO5034A', 'Oscilloscope', 'KeysightInfiniiVisionX'],  # KeysightDSO50bpA
        ['Tektronix', 'TDS7104', 'Oscilloscope', 'TektronixTDS7104'],

        ['Hewlett Packard', '437B', 'PowerMeter', 'HP437B'],
        ['Hewlett Packard', 'E4418B', 'PowerMeter', 'AgilentE4418B'],  # TBC
        ['Agilent Technologies', 'E4418B', 'PowerMeter', 'AgilentE4418B'],
        ['Rohde Schwarz', 'NRVS', 'PowerMeter', 'RohdeSchwarzNRVS'],

        ['Hewlett Packard', '59501B', 'PowerSourceDC', 'HP59501B'],  # No IDN / ID capablity
        ['Agilent Technologies', 'N7972A', 'PowerSourceDC', 'AgilentN7972A'],
        ['TTI', 'PL330P', 'PowerSourceDC', 'TTIPL330P'],  # 'IDN?'?

        ['Marconi Instruments', '2030', 'SignalGenerator', 'MarconiInstruments203N'],
        ['Marconi Instruments', '2031', 'SignalGenerator', 'MarconiInstruments203N'],
        ['Marconi Instruments', '2032', 'SignalGenerator', 'MarconiInstruments203N'],

        ['Rohde Schwarz', 'SMH52', 'SignalGenerator', 'RohdeSchwarzSHM52'],  # 100 kHz to 2 GHz

        ['Hewlett Packard', '8657A', 'SignalGenerator', 'HP8657A'],  # 100 kHz to 1040 MHz

        ['Hewlett Packard', '8664A', 'SignalGenerator', 'HP866nX'],  # 100 kHz to 3 GHz
        ['Hewlett Packard', '8665B', 'SignalGenerator', 'HP866nX'],  # 100 kHz to 6 GHz

        ['Hewlett Packard', '85645A', 'SignalGenerator', 'HP85645A'],  # 300 kHz - 26.5 GHz SG/TG

        ['Hewlett Packard', '83752B', 'SignalGenerator', 'HP83752B'],  # 0.01 - 20 GHz
        # ['Hewlett Packard', '83650B', 'SignalGenerator', 'HP83650B'],  # 0.01 - 50 GHz
        ['Hewlett Packard', '83650B', 'SignalGenerator', 'SCPISignalGenerator'],  # 0.01 - 50 GHz

        ['Hewlett Packard', 'ESG-3000A', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Hewlett Packard', 'ESG-3000B', 'SignalGenerator', 'SCPISignalGenerator'],  # labeled HP, E4421B
        ['Hewlett Packard', 'ESG-4000B', 'SignalGenerator', 'SCPISignalGenerator'],  # labeled HP, E4422B
        
        ['Hewlett Packard', '8648C', 'SignalGenerator', 'SCPISignalGenerator'],  # labeled Agilent, 8648C
        ['Agilent Technologies', '8648C', 'SignalGenerator', 'SCPISignalGenerator'],  # not needed ? HP FW

        ['Hewlett Packard', 'E4421B', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Agilent Technologies', 'E4422B', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Agilent Technologies', 'E4438C', 'SignalGenerator', 'SCPISignalGenerator'],

        ['Keysight Technologies', 'N5173B', 'SignalGenerator', 'SCPISignalGenerator'],

        ['Agilent Technologies', 'N5181A', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Agilent Technologies', 'N5182A', 'SignalGenerator', 'SCPISignalGenerator'],

        ['Anritsu', 'MG3710A', 'SignalGenerator', 'AnritsuMG3710A'],  # VSG as opt

        # MG369nA Series
        ['Anritsu', 'MG3691A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3692A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3693A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3694A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3695A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3696A', 'SignalGenerator', 'AnritsuMG369nAB'],

        # MG369nB Series
        ['Anritsu', 'MG3691B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3692B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3693B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3694B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3695B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3696B', 'SignalGenerator', 'AnritsuMG369nAB'],

        # MG369nC Series
        # SCPI capable, may differ from A,B series

        ['Keysight Technologies', 'N9000B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # CXA
        ['Keysight Technologies', 'N9010B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # EXA
        ['Keysight Technologies', 'N9020B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # MXA
        ['Keysight Technologies', 'N9021B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # MXA
        ['Keysight Technologies', 'N9030B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # PXA
        ['Keysight Technologies', 'N9040B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # UXA
        ['Keysight Technologies', 'N9041B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # UXA
        ['Keysight Technologies', 'N9042B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # UXA

        ['Agilent Technologies', 'E4440A', 'SpectrumAnalyser', 'AgilentE44nn'],  # PSA
        ['Agilent Technologies', 'E4443A', 'SpectrumAnalyser', 'AgilentE44nn'],  # PSA

        ['Hewlett Packard', 'E4406A', 'SpectrumAnalyser', 'AgilentE4406A'],  # VSA

        ['Rohde&Schwarz', 'ESW-8', 'SpectrumAnalyser', 'RaSESW'],

        # 'HP8546A': HP8546A,
        # 'HP8563E': HP8563E,
        # 'HP8564E': HP8564E,
        # 'HP8594E': HP8594E,
        # 'HP8596E': HP8596E,
        # Benchview supported N9040B UXA, N9030A/B PXA, N9020A/B MXA,
        # N9010A/B EXA, N9000A/B CXA, M9290A CXA-m
        # Benchview supported N9320B, N9322C
        # Benchview supported N9342C, N9343C, N9344C
        # Benchview supported E4440A, E4443A, E4445A, E4446A, E4447A, E4448A
        # Benchview supported E4402B, E4404B, E4405B, E4407B
        # Benchview supported E4403B, E4411B, E4408B

        # Agilent Technologies ESA-E Series
        # E4401B (9 kHz- 1.5 GHz)
        # E4402B (9 kHz - 3.0 GHz)
        # E4404B (9 kHz - 6.7 GHz)
        # E4405B (9 kHz - 13.2 GHz)
        # E4407B (9 kHz - 26.5 GHz)
        ['Agilent Technologies', 'E4404B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4401B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4402B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4404B', 'SpectrumAnalyser', 'AgilentE44nn'],
        # FW reports HP, branded Agilent

        ['Hewlett Packard', 'E4405B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4407B', 'SpectrumAnalyser', 'AgilentE44nn'],

        # Agilent Technologies ESA-L Series
        # E4411B (9 kHz- 1.5 GHz)
        # E4403B (9 kHz - 3.0 GHz)
        # E4408B (9 kHz - 26.5 GHz)
        ['Hewlett Packard', 'E4411B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4403B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4408B', 'SpectrumAnalyser', 'AgilentE44nn'],

        ['Hewlett Packard', '8563A', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Hewlett Packard', '8563E', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Hewlett Packard', '8564E', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Hewlett Packard', '8593E', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Hewlett Packard', '8594E', 'SpectrumAnalyser', 'HPGreenScreen'],

        ['Advantest', 'R3172', 'SpectrumAnalyser', 'AdvantestR3172'],

        ['Hewlett Packard', '3488A', 'Switch', 'HP3488A'],

        ['Hewlett Packard', '33120A', 'WaveformGenerator', 'HP33120A'],
        ['Hewlett Packard', '8116A', 'WaveformGenerator', 'HP8116A'],  # 'ID?'?


        ['Thurlby Thandar', 'PL330P', 'PowerSourceDC', 'TTIPL330P'],
        # ['', '', '', '']

    ], columns=['Manufacturer', 'Model', 'Type', 'Driver'])


    def driver_map(self):
        """."""
        self.enumeration = pd.merge(
            self.drivers, self.enumeration, how="right", on=['Manufacturer', 'Model']
        )

    def drivers_sorted(self):
        """."""
        return self.drivers.sort_values(
            ['Type', 'Manufacturer', 'Model']
            ).reset_index()[[
                'Type', 'Manufacturer', 'Model', 'Driver'
            ]]
