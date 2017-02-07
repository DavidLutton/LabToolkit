#!/usr/bin/env python3
import traceback
import sys


def enumerate(rm):
    try:
        pool = {}
        # if rm.list_resources() is not None:
        for resource in rm.list_resources():
            print(resource)

            inst = rm.open_resource(
                resource,
                read_termination='\n',
                write_termination='\r\n' if resource.startswith('ASRL') else '\n'
            )

            try:
                IDN = inst.query("*IDN?")

            except visa.VisaIOError:  # This was found with print(dir(visa))
                traceback.print_exc(file=sys.stdout)
            finally:
                pool[inst] = IDN

        return(rm, pool)
        # print(rm.list_resources())
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
            else:
                pass
    return(alloc)
