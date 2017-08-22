"""."""
import traceback
import sys
import visa
import logging


# visa.log_to_screen()
# pip install --upgrade pip pyvisa pyvisa-sim pyvisa-py pyserial pyusb
# python3 ../attempt.py
# 34401A # meas:volt:dc?, SYST:ERR?
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
