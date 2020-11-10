import numpy as np

from ..GenericInstrument import GenericInstrument


class HP59501B(GenericInstrument):

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = ''
        self.inst.write_termination = ''

    # an.query('*ID?')

    def set(self, vrange, setpoint):
        self.write(f'{vrange}{setpoint}')
