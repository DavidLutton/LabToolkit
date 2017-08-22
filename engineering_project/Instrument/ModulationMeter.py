"""."""
import time
import logging
import pint

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


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


REGISTER = {
    'HEWLETT-PACKARD,8901B': HP8901B,
    'HEWLETT-PACKARD,8901A': HP8901A,
    'Marconi Instuments, 2305': MI2305,

}
