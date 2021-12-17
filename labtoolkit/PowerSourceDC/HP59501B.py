import numpy as np

from ..Instrument import Instrument


class HP59501B(Instrument):

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = ''
        self.inst.write_termination = ''

    # an.query('*ID?')

    def set(self, vrange, setpoint):
        self.write(f'{vrange}{setpoint}')
