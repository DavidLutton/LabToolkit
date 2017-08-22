#!/usr/bin/env python3
import time
import logging

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class SwitchMatrix(GenericInstrument):
    """."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))


class PickeringInterface10(SwitchMatrix):
    """Pickering Interface System 10.

    .. figure::  images/SwitchMatrix/PickeringInterface10.jpg
    """


class HP3488A(SwitchMatrix):
    """HP 3488A Switch/Control Unit.

    .. figure::  images/SwitchMatrix/HP3488A.jpg
    """


REGISTER = {
    "PickeringInterface10": PickeringInterface10,
    "HP3488A": HP3488A,

}
