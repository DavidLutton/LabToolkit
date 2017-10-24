#!/usr/bin/env python3
"""."""

import time
import logging
# import pint

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI

class AudioAnalyser(GenericInstrument):
    """Parent class for AudioAnalyser."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)


class HP8903B(AudioAnalyser):
    """8903B 20 Hz to 100 kHz Audio Analyzer.

    .. figure::  images/AudioAnalyser/HP8903B.jpg
    """


REGISTER = {
    'HEWLETT-PACKARD,8903B': HP8903B,
}
