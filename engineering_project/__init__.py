# -*- coding: utf-8 -*-

__author__ = """David A Lutton"""
__email__ = 'david@dalun.space'
__version__ = '0.1.0'

import visa


from pprint import pprint

import Instrument.PowerMeter
import Instrument.SignalGenerator
import Instrument.WaveformGenerator
import Instrument.SpectrumAnalyser
import Instrument.NetworkAnalyser
import Instrument.ElectronicAttenuator
import Instrument.DigitalMultimeter
import Instrument.EnviromentalChamber
import Instrument.PowerAnalyser
import Instrument.SurgeGenerator
import Instrument.AudioAnalyser
import Instrument.Osciliscope
import Instrument.FieldStrength
import Instrument.Positioner
import Instrument.FrequencyCounter
import Instrument.SourceDC
import Instrument.SourceAC
import Instrument.SwitchMatrix
import Instrument.ModulationMeter
import Instrument.ElectronicLoad

Drivers = [
    Instrument.SignalGenerator,
    Instrument.PowerMeter,
    Instrument.SpectrumAnalyser,
    Instrument.NetworkAnalyser,
    Instrument.AudioAnalyser,
    Instrument.PowerAnalyser,
    Instrument.SurgeGenerator,
    Instrument.FrequencyCounter,
    Instrument.ElectronicAttenuator,
    Instrument.DigitalMultimeter,
    Instrument.Osciliscope,
    Instrument.FieldStrength,
    Instrument.EnviromentalChamber,
    Instrument.Positioner,
    Instrument.SourceDC,
    Instrument.SourceAC,
    Instrument.SwitchMatrix,
    Instrument.ModulationMeter,
    Instrument.WaveformGenerator,
    Instrument.ElectronicLoad,

]

# counter = 0
for each in Drivers:
    pass
    pprint(each)
    pprint(each.REGISTER)
    print()
    # counter += len(each.REGISTER)

Drivernames = []
for driver in Drivers:
    # print(driver)
    Drivernames.append(repr(driver).split("'")[1].split('.')[1])  # Extract class name from repr

# print(counter)

# print(REGISTER)


class ResourceManager(object):
    """ResourceManager as a context manager."""

    def __init__(self, rm):
        self.rm = visa.ResourceManager(rm)

    def __enter__(self):
        return(self.rm)

    def __exit__(self, exc_type, exc, exc_tb):
        del(self.rm)


class Instrument(object):
    """ResourceManager.open_resource as a context manager for instrument."""

    def __init__(self, rm, resource, *, read_termination=False, write_termination=False, **kwargs):

        if read_termination is False:
            read_termination = '\n'
        if write_termination is False:
            write_termination = '\r\n' if resource.startswith('ASRL') else '\n'

        self.inst = rm.open_resource(resource, read_termination=read_termination, write_termination=write_termination, **kwargs)
        # return self.inst

    def __enter__(self):
        # print(repr(self.inst))
        return(self.inst)

    def __exit__(self, *args):
        self.inst.close()


'''
print()
print()

with ResourceManager('@sim') as rm:
    print(rm.list_resources())
    print(rm)

    with Instrument(rm, 'USB::0x1111::0x2222::0x4444::INSTR') as inst:
        # print(inst)
        print(inst.query("*IDN?"))
        # print(inst.session)
    # print(inst.session)
# print(rm.session)
'''
