#!/usr/bin/env python3
"""."""

import time
import logging

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class SwitchMatrix(GenericInstrument):
    """."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")


class PickeringInterface10(SwitchMatrix):
    """Pickering Interface System 10.

    .. figure::  images/SwitchMatrix/PickeringInterface10.jpg
    """


class HP_3488A(SwitchMatrix):
    """HP 3488A Switch/Control Unit.

    .. figure::  images/SwitchMatrix/HP3488A.jpg
    """

    # switcher.switch(502, True)
    # switcher.read(502), switcher.readtext(502)
    # buffer = {}
    # for sw in 100, 101, 102, 103, 110, 111, 112, 113, 200, 201, 202, 203, 210, 211, 212, 213, 300, 301, 302, 303, 310, 311, 312, 313, 400, 401, 402, 500, 501, 502:
    #    buffer[sw] = switcher.read(sw)
    #    print(f"{sw} {switcher.read(sw)}, {switcher.readtext(sw)}")
    # buffer

    # inst.query(f'CTYPE {1}'), inst.query(f'CTYPE {2}'), inst.query(f'CTYPE {3}'), inst.query(f'CTYPE {4}'), inst.query(f'CTYPE {5}')
    # CRESET 1
    # inst.query(f'CMON {4}')
    def __init__(self, inst):
        self.inst = inst
        self.inst.read_termination = '\r\n'
        self.inst.write_termination = '\n'

    def switch(self, switch, state):
        if state in ['OPEN', False]:
            self.inst.write(f'OPEN {switch}')

        if state in ['CLOSE', True]:
            self.inst.write(f'CLOSE {switch}')

    def viewtext(self, switch):
        return self.inst.query(f'VIEW {switch}').split(' ')[0]  # 'CLOSED 0', 'OPEN 1'

    def view(self, switch):
        # 'CLOSED 0', 'OPEN 1'
        if int(self.inst.query(f'VIEW {switch}').split(' ')[-1]) == 1:
            return bool(False)
        else:
            return bool(True)


REGISTER = {
    # "PickeringInterface10": PickeringInterface10,
    # "HP3488A": HP_3488A,

}
