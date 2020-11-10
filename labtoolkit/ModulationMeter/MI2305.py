# import visa

# rm = visa.ResourceManager()
# print(rm.list_resources())

 
# inst = rm.open_resource('GPIB0::5::INSTR')

# print( inst.query('TM').strip() )
# print( inst.query('TF').strip() )
# 'Marconi Instuments, 2305': MI2305,

from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class MI2305(IEEE488):  # GenericInstrument
    """."""

    def __init__(self, inst):
        """."""
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self.inst.timeout = 5000

    pass
