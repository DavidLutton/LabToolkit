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


class HP_8901B(ModulationMeter):
    """HP 8901B. Modulation Analyser, 150e3 to 1.3e9"""

    def __init__(self, inst):
        self.inst = inst
        self.inst.timeout = 6000  # Extend the default timeout as it can take a few seconds to get a settled reading
        self.inst.read_termination = '\r\n'
        self.inst.write_termination = '\n'
        # instMM.query('ID')  # 8901.2

    def MeasureFM(self):
        """."""
        # generator = FunctionName(inst)
        # Inital call of next(generator) runs the init/setup, when next is called the first time
        # RST ?
        self.inst.write('IP AU M2 H1 L1 D9')  # Preset, Auto, Measure FM, Highpass 1 (50Hz), Lowpass 1 (3kHz), Detector 9 (Peak ± / 2)

        # Using next(generator) and subsequent calls to next(generator) yields a measurement

        # A subsequent call to the generator.send() allows input of infomation to the generator
        # The input of the generator.send(input) will be the result of the yield statement
        # x in this case

        x = None  # Using None allows you to not have to use generator.send(None) when you don't have data to input
        # This allows for a not None to be used as a flow control

        while x is None:
            # x = yield float(self.inst.query('T3'))  # Trigger with settling
            x = yield float(self.inst.query('T0', delay=4))  # Delay reading result so that a settled measurment is recorded

        # When x is set to anything other than None, and the while loop finishes in that state this (↓) will be reached
        self.inst.write('T0')  # Free run
        yield False

    def MeasureAM(self):
        """."""
        # generator = FunctionName(inst)
        # Inital call of next(generator) runs the init/setup, when next is called the first time
        self.inst.write('IP AU M1 H1 L1 D9')  # Preset, Auto, Measure AM, Highpass 1 (50Hz), Lowpass 1 (3kHz), Detector 9 (Peak ± / 2)

        # Using next(generator) and subsequent calls to next(generator) yields a measurement

        # A subsequent call to the generator.send() allows input of infomation to the generator
        # The input of the generator.send(input) will be the result of the yield statement
        # x in this case

        x = None  # Using None allows you to not have to use generator.send(None) when you don't have data to input
        # This allows for a not None to be used as a flow control

        while x is None:
            # x = yield float(self.inst.query('T3'))  # Trigger with settling
            # print(inst.query('T0'))
            # print(inst.read())
            # print(inst.read())
            # x = yield float(self.inst.read())
            # T0 Free Run
            # T1 Hold
            # T3 trig
            x = yield float(self.inst.query('T0', delay=4))  # Delay reading result so that a settled measurment is recorded

        # When x is set to anything other than None, and the while loop finishes in that state this (↓) will be reached
        self.inst.write('T0')  # Free run
        yield False  # f'tidyed up {self.__name__}'


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
    'HEWLETT-PACKARD,8901B': HP_8901B,
    'HEWLETT-PACKARD,8901A': HP8901A,
    'Marconi Instuments, 2305': MI2305,

}
