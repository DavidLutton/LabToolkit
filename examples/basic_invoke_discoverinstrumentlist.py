from pprint import pprint

import labtoolkit as labtk

with labtk.ResourceManager('') as rm:
    reso = rm.list_resources()
    # reso = ['GPIB0::16::INSTR', 'GPIB0::17::INSTR', 'GPIB0::22::INSTR']
    pprint(reso)
    for ignore in ['ASRL', 'GPIB0::18', 'GPIB0::6']:  # Ignore list
        reso = [x for x in reso if not x.startswith(ignore)]
    pprint(reso)

    pool = labtk.visaenumerate(rm, reso)
    pprint(pool)

    instrument = labtk.Instruments()  # Empty Instruments object
    for driver in labtk.driverclasses:
        # Each driverclass can register a driver for every instrument
        pod = labtk.driverdispatcher(pool, getattr(labtk, driver).REGISTER)
        if len(pod) != 0:
            setattr(instrument, driver, pod)

    pprint(instrument)

    # print(instrument.SignalGenerator[0].frequency) # Get current frequency
    # instrument.SignalGenerator[0].frequency = 2e9  # Set frequency to 2GHz
