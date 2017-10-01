#!/usr/bin/env python3

# import pint

try:
    from labtoolkit.GenericInstrument import GenericInstrument
    from labtoolkit.IEEE488 import IEEE488
    from labtoolkit.SCPI import SCPI

except ImportError:
    from GenericInstrument import GenericInstrument
    from IEEE488 import IEEE488
    from SCPI import SCPI


# ureg = pint.UnitRegistry()
# ureg.default_format = '~P'
# Q_ = ureg.Quantity


class Positioner(GenericInstrument):

    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))


class AnaheimAutomationSMC40(Positioner):

    # http://www.anaheimautomation.com/manuals/stepper/L010098%20-%20SMC40%20Users%20Guide.pdf

    def __init__(self, instrument):
        super().__init__(instrument)

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    @property
    def heading(self):
        return NotImplemented

    @heading.setter
    def heading(self, clockwise=True):
        if clockwise is True:
            self.write('D+')  # Clockwise
        else:
            self.write('D-')  # Anti-Clockwise

    @property
    def stepangle(self):
        return NotImplemented

    @stepangle.setter
    def stepangle(self, stepangle=1):  # 100 is 1 degree
        self.write('XMN{}'.format(int(stepsize*100)))
        # int(Q_(stepangle, 'degree').magnitude * 100)
        # self.write('XMN{}'.format(int(Q_(stepangle, 'degree').magnitude * 100)))

    def zero(self):
        self.write('XGH')

    def init(self):
        self.write('@0')

    def IDN(self):
        return self.query('ID')

    def WAI(self):
        return self.query('XMC')  # ??

    def TRG(self):
        self.write('XGR')

    def move(self, clockwise=True, angle=1, wait=True):
        self.stepsize = angle
        self.heading = clockwise
        self.write('XGR')
        if wait is True:
            self.WAI()


REGISTER = {
    'SMC40': AnaheimAutomationSMC40,

}
