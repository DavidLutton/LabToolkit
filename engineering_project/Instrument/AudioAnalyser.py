#!/usr/bin/env python3
"""."""

import time
import logging
import pint

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class AudioAnalyser(GenericInstrument):
    """Parent class for AudioAnalyser."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)


class HP8903B(AudioAnalyser):
    """8903B 21 Hz to 100 kHz Audio Analyzer."""


REGISTER = {
    'HEWLETT-PACKARD,8903B': HP8903B,
}
