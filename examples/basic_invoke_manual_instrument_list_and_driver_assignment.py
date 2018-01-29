
from pprint import pprint  # https://docs.python.org/3/library/pprint.html
import time

import labtoolkit as labtk

with labtk.ResourceManager('') as rm:

    SignalGenerator = labtk.SignalGenerator.HP8657A(
        rm.open_resource(
            'GPIB0::10::INSTR', read_termination='\n', write_termination='\n')
    )
    PowerMeter = labtk.PowerMeter.RohdeSchwarzNRVS(
        rm.open_resource(
            'GPIB0::8::INSTR', read_termination='\n', write_termination='\n')
    )

    SignalGenerator.frequency = 1e6
    SignalGenerator.amplitude = -10
    SignalGenerator.output = True
    time.sleep(1)
    print(PowerMeter.measurement)
