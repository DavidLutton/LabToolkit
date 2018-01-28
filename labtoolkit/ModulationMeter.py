#!/usr/bin/env python3
"""."""
import time
import logging
# import pint

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class ModulationMeter(GenericInstrument):
    """Parent class for ModulationMeter."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)


class HP8901B(ModulationMeter):
    """8901B Modulation Analyzer, 150e3 to 1.3e9."""


class HP8901A(ModulationMeter):
    """."""


class MI2305(ModulationMeter):
    """."""

    '''
    inst = rm.open_resource('GPIB0::5::INSTR')
    print( inst.query('TM').strip() )
    print( inst.query('TF').strip() )
    '''


REGISTER = {
    'HEWLETT-PACKARD,8901B': HP8901B,
    'HEWLETT-PACKARD,8901A': HP8901A,
    'Marconi Instuments, 2305': MI2305,

}
