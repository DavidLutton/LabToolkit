# inst = rm.open_resource('GPIB0::5::INSTR')

# print( inst.query('TM').strip() )
# print( inst.query('TF').strip() )

from ..IEEE488 import IEEE488


class MI2305(IEEE488):  # GenericInstrument
    """."""

    
    pass
