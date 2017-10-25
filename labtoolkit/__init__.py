# -*- coding: utf-8 -*-

__author__ = """David A Lutton"""
__email__ = 'david@dalun.space'
__version__ = '0.1.0'

import sys

import visa

from pprint import pprint

from . import PowerMeter
from . import SignalGenerator
from . import WaveformGenerator
from . import SpectrumAnalyser
from . import NetworkAnalyser
from . import ElectronicAttenuator
from . import DigitalMultimeter
from . import EnviromentalChamber
from . import PowerAnalyser
from . import SurgeGenerator
from . import AudioAnalyser
from . import Osciliscope
from . import FieldStrength
from . import Positioner
from . import FrequencyCounter
from . import SourceDC
from . import SourceAC
from . import SwitchMatrix
from . import ModulationMeter
from . import ElectronicLoad
# from . import PortableApplianceTester


def what():
    for name in set(sys.modules):
        if name.startswith(__name__):

            module = sys.modules[name]
            try:
                pprint(module.REGISTER)
                print()
            except AttributeError:
                pass


driverclasses = []
for name in set(sys.modules):
    if name.startswith(__name__+'.'):
        module = (sys.modules[name])
        try:
            if module.REGISTER:  # has drivers
                name = module.__name__.split('.')[1]
                # print(name)
                driverclasses.append(name)
        except AttributeError:
            pass

# pprint(driverclasses)


class ResourceManager(object):
    """ResourceManager as a context manager."""

    def __init__(self, rm):
        self.rm = visa.ResourceManager(rm)

    def __enter__(self):
        return(self.rm)

    def __exit__(self, exc_type, exc, exc_tb):
        del(self.rm)


class Instrument(object):
    """Instrument.open_resource as a context manager."""

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


def visaaddresslist(listofaddresses, prefix="GPIB0", suffix="65535::INSTR"):
    """Generate full address for list of bus address.

    :param listofaddresses: list of integers which are instrument addresses
    :param prefix: prefix for the bus
    :param suffix: suffix for the bus
    :returns: list of fully formed address of instuments
    """
    instrs = []
    for inst in listofaddresses:
        instrs.append("{}::{}::{}".format(prefix, inst, suffix))
    return(instrs)


#  'TCPIP::192.168.1.113::INSTR'


def visaenumerate(rm, list_resources):
    """Try to discover IDNs for autodiscoverd instruments on a bus."""
    try:
        pool = {}
        # if rm.list_resources() is not None:
        for resource in list_resources:
            # print(resource)

            inst = rm.open_resource(
                resource,
                read_termination='\n',
                write_termination='\r\n' if resource.startswith('ASRL') else '\n'
            )

            try:
                query = "*IDN?"
                response = inst.query(query)
                # log.debug("Query {}:{} {}".format(resource, query, response))
                IDN = response

            except visa.VisaIOError:  # This was found with print(dir(visa))
                pass  # traceback.print_exc(file=sys.stdout)
                IDN = "NONE"
            finally:
                pool[inst] = IDN

        return(pool)
    except ValueError:
        pass
    except OSError:
        pass
    except FileNotFoundError:
        print("File for SIM not found")


def driverdispatcher(pool, driverlist):
    """Pair IDN with corresponding driver class."""
    alloc = {}
    insts = 0
    for inst in pool:
        for driver in driverlist:
            if pool[inst].startswith(driver):
                alloc[insts] = driverlist[driver](inst)
                insts += 1
    return(alloc)


class Instruments(object):

    def __repr__(self):
        # return str(self.__dict__)
        buffer = []
        for key, value in instrument.__dict__.items():
            buffer.append('{}:'.format(key))
            for valu in value:
                buffer.append('     {}: {}'.format(valu, value[valu]))
        return str('\n'.join(buffer))


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
