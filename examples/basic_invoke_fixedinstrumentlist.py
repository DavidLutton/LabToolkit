from pprint import pprint  # https://docs.python.org/3/library/pprint.html

import labtoolkit as labtk

with labtk.ResourceManager('') as rm:
    # reso = rm.list_resources()
    reso = ['GPIB0::07::INSTR', 'GPIB0::04::INSTR']
    pprint(reso)
    pool = labtk.visaenumerate(rm, reso)
    # pprint(pool)

    instrument = labtk.Instruments()  # Empty Instruments object
    for driverclass in labtk.driverclasses:
        # Each driverclass can register a driver for every instrument
        pod = labtk.driverdispatcher(pool, getattr(labtk, driverclass).REGISTER)
        if len(pod) != 0:
            setattr(instrument, driverclass, pod)

    pprint(instrument)

    # Example output from last pprint
    '''
    SignalGenerator:
        0: AnritsuMG3691B, GPIBInstrument at GPIB0::07::INSTR
    SpectrumAnalyser:
        0: HPE4406A, GPIBInstrument at GPIB0::04::INSTR
    '''
