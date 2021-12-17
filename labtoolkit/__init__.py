"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.


.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import abc
import importlib
import logging

import pandas as pd
import pyvisa

from time import sleep


# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
# logger.info(f'Invoking __init__.py for {__name__}')
# logger.level(0)


# from .Utils.frequency import FrequencyGroup, HarmonicMixer, SourceMultiplier, FrequencySweep
# from .Utils.testrecorder import TestRecorder
# from .Utils.get import get_bytes, get_file, get_latest, get_powerhead_factors, get_testspec
# from .Utils.enumerate import drivers_list, drivers_show, enumerate_instruments
# from .Utils.modulation import Modulation


class Enumerate(metaclass=abc.ABCMeta):
    def __init__(self, rm, ignores, additives,*, appendix):
        self.rm = rm
        
        # add resources in appendix to ignore (for enumerate_resources list)
        
        # if not appendix.empty:
        #  ignores = [resource for resource in res*** if resource in list(appendix['Resource'])]

        self.enumeration = self.enumerate_resources(ignores, additives)
        
        # interject insts that don't respond to *IDN?
        if not appendix.empty:
            self.enumeration = pd.concat(
                [self.enumeration, appendix],
                axis=0,
                join='outer',
                ignore_index=True
            )
        
        self.driver_map()
        # display(self.enumeration)
        self.driver_load()

        self.__post__()
        # return self.enumeration
   
    def __post__(self):
        pass


    def driver_load(self):
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
      
    def enumerate_resources(self, ignores=[], additives=[]):
        resources = self.rm.list_resources() + tuple(additives)
        # resources = rm.list_resources() + additives
        resources = [resource for resource in resources if resource not in ignores]
        
        mapping = pd.DataFrame(columns=['Manufacturer', 'Model'])
        for number, resource in enumerate(resources):

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

                    parts[0] = parts[0].title().replace('-', ' ')
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
                        # mapping.loc[number, 'Serial'] = '0'
                    if ID == 'HP8594E\r':
                        mapping.loc[number, 'Resource'] = resource
                        mapping.loc[number, 'IDN'] = 'Hewlett Packard, 8594E, 0, 0'
                        mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
                        mapping.loc[number, 'Model'] = '8594E'  # 401 pts
                        # mapping.loc[number, 'Serial'] = '0'
                        
                    if ID == 'HP8593E\r':
                        mapping.loc[number, 'Resource'] = resource
                        mapping.loc[number, 'IDN'] = 'Hewlett Packard, 8593E, 0, 0'
                        mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
                        mapping.loc[number, 'Model'] = '8593E'  # 401 pts
                        # mapping.loc[number, 'Serial'] = '0'
                
                if IDN == None: 
                    print('None,None')
                    logger.warning(f'{resource} ...')
                    ID = inst.query('ID?')
                    logger.warning(f'{resource} {ID}')
                    if ID == 'E8563E': # TODO how to ID, no trailing \r
                        mapping.loc[number, 'Resource'] = resource
                        mapping.loc[number, 'IDN'] = 'Hewlett Packard, 8563E, 0, 0'
                        mapping.loc[number, 'Manufacturer'] = 'Hewlett Packard'
                        mapping.loc[number, 'Model'] = '8563E'  # 601 pts
                        # mapping.loc[number, 'Serial'] = '0'
                
            
            except IndexError:
                pass
            
            except pyvisa.VisaIOError as e:
                logger.warning(e)
                # if e == : 
                # VI_ERROR_RSRC_NFOUND
                # VI_ERROR_NLISTENERS
                # VI_ERROR_TMO
                '''
                if e.error_code == pyvisa.errors.VI_ERROR_TMO:
                    sleep(.25)

                    RSIDN = inst.query('ZV')
                    if RSIDN.startswith('ROHDE & SCHWARZ NRVS VER.:'):
                        mapping.loc[number, 'Resource'] = resource
                        mapping.loc[number, 'IDN'] = 'Rohde Schwarz,NVRS,0,0'
                        mapping.loc[number, 'Manufacturer'] = 'Rohde Schwarz'
                        mapping.loc[number, 'Model'] = 'NVRS'
                '''

            finally:
                try:
                    # display(mapping)
                    inst.close()
                except NameError:
                    # Don't raise an error if you cannot close a inst, that probably never opened
                    # NI VISA 20 reports disconnected end points, when you don't refresh scan for connected HW
                    pass

         # print(f'{resource} {e}')

        return mapping.reset_index(drop=True)


    drivers = pd.DataFrame([
        ['Marconi Instruments', '2187', 'Attenuator', 'MI2187'],
        ['MI Wave', '511', 'Attenuator', 'MIWave5nn'],
           
        ['Hewlett Packard', '8903B', 'AudioAnalyser', 'HP8903B'],

        ['Hewlett Packard', '34401A', 'DigitalMultimeter', 'HP34401A'],
        ['Hewlett Packard', '3457A', 'DigitalMultimeter', 'HP3457A'],

        # http://www.eevblog.com/forum/metrology/raspberry-pi23-logging-platform-for-voltnuts/350/
        # HP 34401A/3446xA
        # HP 3458A (can test this)
        # Keithley 2000
        # Keithley 2001/2002 (can test this with both 2001 and 2002)
        # Keithley 2510 TEC SMU
        # Keithley 2001, 2002, 2400, 2510, 182, HP 3458, Wavetek 4920/4920M.
        # LAN for Keithley DMM7510, Tek DMM4050/Fluke 8846A and Keysight 3446xA/34470A.
        # Rigol DM3068
        # Keysight 34461A, 
        # Rigol DM3068 over LAN.
        # Agilent E5810A
        # 3458A,K2001,K2002
        # 3441xA/34401A/3446xA
        # Keysight 34461A over either LAN or USB, please.
        # I have an HP3456A and Agilent HPIB to USB interface on the way. Also have RP3.
        # I also have an 3456 on the way and a Agilent 82357B clone, 2xBME280 on the way, all to join the K2000 and the 3457.
        # So for me would be great in the 3456/7 could be add to the list.
        # I have a recent 3458A (Firm. Rev. 9.2), 34470A and Keithley 2000
        # If I remember K2001 and K2002 have 3458A GPIB compatibility mode ... so supporting 3458A means also K2001 and K2002.
        # HP3478A
        # Keithley 2000
        # DP832
        # TEK TDS5052B
        # HP3245A
        # FLUKE 87V
        # HP33120A
        # 34461A - Agilent
        # 34410A - Agilent
        # DMM7510 - Keithley
        # 2450 SMU - Keithley
        # DM3068 - Rigol
        # KEITHLEY INSTRUMENTS INC.,MODEL 6517B,1234567,A13/700x
        # Agilent Technologies,34411A,MY12345678,2.41-2.40-0.09-46-09
        # KEITHLEY INSTRUMENTS INC.,MODEL 2001M,1234567,B17  /A02
        # HM8012
        # HM8012 benchtop multimeter with RS232, 
        # a RK8511 DC electronic load with RS232
        # a Siglent SPD3303D power supply with an USB po
        # BME280
        # Rigol DM3068
        # KEITHLEY INSTRUMENTS INC.,MODEL 2015,1043877,B15  /A02
        # SPD3303D power supply.
        # Siglent Technologies,SPD3303,SPD00002130137,1.01.01.01.05,V1.1
        # Rigol DM3068
        # SPD3303
        # KEITHLEY INSTRUMENTS INC.,MODEL 2015,1043877,B15  /A02
        # Agilent Technologies,34411A,MY12345678,2.41-2.40-0.09-46-09
        # Siglent Technologies,SPD3303,SPD00002130137,1.01.01.01.05,V1.1

        # Rigol DM3068
        # Keysight U1272a
        # benchview supported 
        # 34401A, 34405A, 34410A, 34411A, 34420A, 34450A, 34460A, 34461A, 34465A, 34470A

        
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

        # Benchview suppored:
        # ENA:  E5080A, E5061B, E5063A, E5071C, E5072A
        # PNA:  N5221A, N5222A, N5224A, N5245A, N5227A
        # PNA-L:  N5230C, N5231A, N5232A, N5234A, N5235A, N5239A
        # PNA-X:  N5241A, N5242A, N5244A, N5245A, N5247A, N5249A
        # Fieldfox: N9912A, N9913A, N9914A, N9915A, N9916A, N9917A, N9918A, N9923A, N9925A,
        #  N9926A, N9927A, N9928A, N9935A, N9936A, N9937A, N9938A, N9950A, N9951A, N9952A, N9960A, N9961A, N9962A
        
        ['Keysight Technologies', '3034T', 'Oscilloscope', 'KeysightInfiniiVisionX'],
        ['Agilent Technologies', 'DSO5052A', 'Oscilloscope', 'AgilentDSO50nnA'],  # KeysightDSO50bpA
        ['Agilent Technologies', 'DSO5034A', 'Oscilloscope', 'AgilentDSO50nnA'],  # KeysightDSO50bpA
        ['Tektronix', 'TDS7104', 'Oscilloscope', 'TektronixTDS7104'],
        # Benchview supported DSO6054L, DSO6104L, DSO6104L, DSO5014A, DSO5032A, DSO5034A, DSO5052A, DSO5054A, DSO6012A, DSO6014A, DSO6014L, DSO6032A, DSO6034A, DSO6052A, DSO6054A, DSO6054L, DSO6102A,
        #                     DSO6104A, DSO6104L, DSO7012A, DSO7012B, DSO7014A, DSO7014B, DSO7032A, DSO7032B, DSO7034A, DSO7034B, DSO7052A, DSO7052B, DSO7054A, DSO7054B, DSO7104A, DSO7104B, DSO90254A,
        #                     DSO90404A, DSO90604A, DSO9064A, DSO90804A, DSO9104A, DSO91204A, DSO91304A, DSO9254A, DSO9404A, DSOS054A, DSOS104A, DSOS204A, DSOS254A, DSOS404A, DSOS604A, DSOS804A,
        # Benchview supported DSO-X 2002A, DSO-X 2004A, DSO-X 2012A, DSO-X 2014A, DSO-X 2022A, DSO-X 2024A, DSO-X 3012A, DSO-X 3012T, DSO-X 3014A, DSO-X 3014T, DSO-X 3022T, DSO-X 3024A, DSO-X 3024T,
        #                     DSO-X 3032A, DSO-X 3032T, DSO-X 3034A, DSO-X 3034T, DSO-X 3052A, DSO-X 3052T, DSO-X 3054A, DSO-X 3054T, DSO-X 3102A, DSO-X 3102T, DSO-X 3104A, DSO-X 3104T, DSO-X 4022A,
        #                     DSO-X 4024A, DSO-X 4032A, DSO-X 4034A, DSO-X 4052A, DSO-X 4054A, DSO-X 4104A, DSO-X 4154A,
        # Benchview supported DSOX1102A, DSOX1102G, DSOX6002A , DSOX6004A , DSOX91304A, DSOX91604A, DSOX92004A, DSOX92004Q, DSOX92504A, DSOX92504Q, DSOX92804A, DSOX93204A,
        #                     DSOX93304Q, DSOX95004Q, DSOX96204Q
        # Benchview supported EDUX1002A, EDUX1002G,
        # Benchview supported MSO6012A, MSO6014A, MSO6032A, MSO6034A, MSO6052A, MSO6054A, MSO6102A, MSO6104A, MSO7012A, MSO7012B, MSO7014A, MSO7014B, MSO7032A, MSO7032B, MSO7034A, MSO7034B, MSO7052A,
        #                     MSO7052B, MSO7054A, MSO7054B, MSO7104A, MSO7104B, MSO9064A, MSO9104A, MSO9254A, MSO9404A, MSOS054A, MSOS104A, MSOS204A, MSOS254A, MSOS404A, MSOS604A, MSOS804A,
        # Benchview supported MSO-X 2002A, MSO-X 2004A, MSO-X 2012A, MSO-X 2014A, MSO-X 2022A, MSO-X 2024A, MSO-X 3012A, MSO-X 3012T, MSO-X 3014A, MSO-X 3014T, MSO-X 3022T,
        #                     MSO-X 3024A, MSO-X 3024T, MSO-X 3032A, MSO-X 3032T, MSO-X 3034A, MSO-X 3034T, MSO-X 3052A, MSO-X 3052T, MSO-X 3054A, MSO-X 3054T, MSO-X 3102A, MSO-X 3102T, MSO-X 3104A,
        #                     MSO-X 3104T, MSO-X 4022A, MSO-X 4024A, MSO-X 4032A, MSO-X 4034A, MSO-X 4052A, MSO-X 4054A, MSO-X 4104A, MSO-X 4154A,
        # Benchview supported MSOX6002A , MSOX6004A , MSOX91304A, MSOX91604A, MSOX92004A, MSOX92504A, MSOX92804A, MSOX93204A

        ['Hewlett Packard', '437B', 'PowerMeter', 'HP437B'],
        ['Hewlett Packard', 'E4418B', 'PowerMeter', 'AgilentE4418B'],  # TBC
        ['Agilent Technologies', 'E4418B', 'PowerMeter', 'AgilentE4418B'],
        ['Rohde Schwarz', 'NVRS', 'PowerMeter', 'RohdeSchwarzNRVS'],


        # Bird 4421
        # Benchview Supported N1911A, N1912A, N1913A, N1914A, N8262A,
        # Benchview Supported 
        # U2000A, U2000B, U2000H, U2001A, U2001B, U2001H, U2002A, U2002H, 
        # U2004A, U2021XA, U2022XA, U2041XA, U2042XA, U2043XA, U2044XA,
        # U2049XA LAN, U8481A, U8485A, U8487A, U8488A
            
        # "CaliforniaInstruments3000i": CaliforniaInstruments3000i,
        # "CaliforniaInstruments3000iM": CaliforniaInstruments3000iM,
        # 'SchaffnerNSG1007': SchaffnerNSG1007,
        # 'Yac...': YA
        
        ['Hewlett Packard', '59501B', 'PowerSourceDC', 'HP59501B'],  # No IDN / ID capablity
        ['Agilent Technologies', 'N7972A', 'PowerSourceDC', 'AgilentN7972A'],
        ['TTI', 'PL330P', 'PowerSourceDC', 'TTIPL330P'],  # 'IDN?'?
            
        # 'THURLBY THANDAR,MX100TP,': TTIMX100TP,
        # 'THURLBY THANDAR,MX180TP,': TTIMX180TP,
        # TTI, CPX400DP
        # 'Rohde & Schwarz, HMC8043,':
        # 'Rohde & Schwarz, HMC8042,':
        # 'Rohde & Schwarz, HMC8041,':
        # Keithley, 2231A-30-3
        # Keithley, 2220-30-1
        # BKPrecision, BK9130B
        # BKPrecision, BK9181B
        # Keysight, E3648A
        # Keysight, E3634A
        # Keysight, E3649A
        # Keysight, E3631A
        # Keysight, E3644A
        # Keysight, E36104A
        # GWINSTEK, GPD-4303S
        # GWINSTEK, GPD-2303S
        # Keithley, 2220-30-1
        # Benchview supported E3631A, E3632A, E3633A, E3634A, E3640A, E3641A, E3642A, E3643A, E3644A, E3645A, E3646A, E3647A, E3648A, E3649A, E36102A, E36103A, E36104A, E36105A, E36106A, E36310A,
        # Benchview supported E36311A, E36312A, E36313A, N6700A/B/C,
        # Benchview supported N6701A/C, N6702A/C, N6705A/B/C, N6950A, N6951A, N6952A, N6953A, N6954A, N6970A, N6971A, N6972A, N6973A, N6974A, N6976A, N6977A, N7950A, N7951A, N7952A, N7953A, N7954A,
        # Benchview supported N7970A, N7971A, N7972A, N7973A, N7974A, N7976A, N7977A, N6785A, N6786A, B2901A, B2902A,
        # Benchview supported B2911A,B2912A, B2961A, B2962A, N5741A, N5742A, N5743A, N5744A, N5745A, N5746A, N5747A, N5748A, N5749A, N5750A, N5751A, N5752A, N5761A, N5762A, N5763A, N5764A,
        # Benchview supported N5765A, N5766A, N5767A, N5768A, N5769A, N5770A, N5771A, N5772A, N8731A, N8732A, N8733A, N8734A, N8735A, N8736A, N8737A, N8738A, N8739A, N8740A, N8741A, N8742A,
        # Benchview supported N8754A, N8755A, N8756A, N8757A, N8758A, N8759A, N8760A, N8761A, N8762A, N8920A, N8921A, N8922A, N8923A, N8924A, N8925A, N8926A, N8927A, N8928A, N8929A, N8930A,
        # Benchview supported N8931A, N8932A, N8933A, N8934A, N8935A, N8936A, N8937A, N8940A, N8941A, N8942A, N8943A, N8944A, N8945A, N8946A, N8947A, N8948A, N8949A, N8950A, N8951A, N8952A,
        # Benchview supported N8953A, N8954A, N8955A, N8956A, N8957A, N6731B, N6732B, N6733B, N6734B, N6735B, N6736B, N6741B, N6742B, N6743B, N6744B, N6745B, N6746B, N6773A, N6774A, N6775A,
        # Benchview supported N6776A, N6777A, N6751A, N6752A, N6753A, N6754A, N6755A, N6756A, N6761A, N6762A, N6763A, N6764A, N6765A, N6766A, N6781A, N6782A, N6784A, N6785A, N6786A, N6783A-BAT, N6783A-MFG

        
        ['Marconi Instruments', '2030', 'SignalGenerator', 'MarconiInstruments203N'],
        ['Marconi Instruments', '2031', 'SignalGenerator', 'MarconiInstruments203N'],
        ['Marconi Instruments', '2032', 'SignalGenerator', 'MarconiInstruments203N'],
        
        ['Rohde Schwarz', 'SMH52', 'SignalGenerator', 'RohdeSchwarzSHM52'],  # 100 kHz to 2 GHz
        
        ['Hewlett Packard', '8657A', 'SignalGenerator', 'HP8657A'],  # 100 kHz to 1040 MHz

        ['Hewlett Packard', '8664A', 'SignalGenerator', 'HP866nX'],  # 100 kHz to 3 GHz
        ['Hewlett Packard', '8665B', 'SignalGenerator', 'HP866nX'],  # 100 kHz to 6 GHz
                      
        ['Hewlett Packard', '85645A', 'SignalGenerator', 'HP85645A'],  # 300 kHz - 26.5 GHz SG/TG

        ['Hewlett Packard', '83752B', 'SignalGenerator', 'HP83752B'],  # 0.01 - 20 GHz
        ['Hewlett Packard', '83650B', 'SignalGenerator', 'HP83650B'],  # 0.01 - 50 GHz
        
        ['Hewlett Packard', 'ESG-3000A', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Hewlett Packard', 'ESG-3000B', 'SignalGenerator', 'SCPISignalGenerator'],  # labeled HP, E4421B 
        ['Hewlett Packard', 'ESG-4000B', 'SignalGenerator', 'SCPISignalGenerator'],  # labeled HP, E4422B 
        
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
        # Benchview supported E4438C, E4428C, E8267D, E8257D, E8663D, N5171B,N5172B, N5173B, N5181A/B, N5182A/B, N5183A/B

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
        
        ['Hewlett Packard', 'E4406A', 'SpectrumAnalyser', 'AgilentE4406A'],  # VSA
        
        
        
        # 'HP8546A': HP8546A,
        # 'HP8563E': HP8563E,
        # 'HP8564E': HP8564E,
        # 'HP8594E': HP8594E,
        # 'HP8596E': HP8596E,
        # Benchview supported N9040B UXA, N9030A/B PXA, N9020A/B MXA, N9010A/B EXA, N9000A/B CXA, M9290A CXA-m
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
        ['Hewlett Packard', 'E4404B', 'SpectrumAnalyser', 'AgilentE44nn'],  # FW reports HP, branded Agilent
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
        
        # Benchview suppored 33210A, 33220A, 33250A, 33521A, 33522A, 33509B,
        # 33510B, 33511B, 33512B, 33519B, 33520B, 33521B, 
        # 33522B, 33611A, 33612A, 33621A, 33622A, 81150A, 81160A


        # ['', '', '', '']
        
   ], columns=['Manufacturer', 'Model', 'Type', 'Driver'])


    def driver_map(self):
        self.enumeration = pd.merge(
            self.drivers, self.enumeration, how="right", on=['Manufacturer', 'Model']
        )

    def drivers_sorted(self):
        return self.drivers.sort_values(['Type', 'Manufacturer', 'Model']).reset_index()[['Type', 'Manufacturer', 'Model', 'Driver']]