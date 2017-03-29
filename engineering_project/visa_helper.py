#!/usr/bin/env python3
import traceback
import sys
import visa
import logging


# visa.log_to_screen()
# pip install --upgrade pip pyvisa pyvisa-sim pyvisa-py pyserial pyusb
# python3 ../attempt.py
# 34401A # meas:volt:dc?, SYST:ERR?
def visaaddresslist(listofaddresses, prefix="GPIB0::", suffix="::65535::INSTR"):
        instrs = []
        for inst in listofaddresses:
            instrs.append("{}{}{}".format(prefix, inst, suffix))
        return(instrs)


def visaenumerate(rm, list_resources):
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
    alloc = {}
    insts = 0
    for inst in pool:
        for driver in driverlist:
            if pool[inst].startswith(driver):
                alloc[insts] = driverlist[driver](inst)
                insts += 1
    return(alloc)


class ResourceManager(object):
    def __init__(self, rm):
        self.rm = visa.ResourceManager(rm)

    def __enter__(self):
        return(self.rm)

    def __exit__(self, exc_type, exc, exc_tb):
        del(self.rm)


class Instrument(object):
    def __init__(self, rm, resource_name, read_termination='\n', write_termination='\n', **kwargs):
        self.inst = rm.open_resource(resource_name, read_termination=read_termination, write_termination=write_termination, **kwargs)
        # return(self.inst)

    def __enter__(self):
        # print(repr(self.inst))
        return(self.inst)

    def __exit__(self, exc_type, exc, exc_tb):
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
