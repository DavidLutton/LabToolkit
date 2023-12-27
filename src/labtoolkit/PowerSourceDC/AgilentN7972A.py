import numpy as np
import pandas as pd

from ..IEEE488 import IEEE488
from ..SCPI import SCPI

from time import sleep


class AgilentN7972A(IEEE488, SCPI):
    """."""

    @property
    def voltage(self):
        """."""
        return self.query_float('VOLTage?')

    @voltage.setter
    def voltage(self, voltage):
        self.write(f'VOLTage {voltage:.4f}')

    @property
    def current_limit(self):
        """."""
        return self.query_float(':SOURce:CURRent:LIMit:POSitive:IMMediate:AMPLitude?')

    @current_limit.setter
    def current_limit(self, current):
        self.write(f':SOURce:CURRent:LIMit:POSitive:IMMediate:AMPLitude {current}')

    @property
    def output(self):
        """."""
        return self.query_bool(':OUTPut:STATe?')

    @output.setter
    def output(self, state):
        self.write(f':OUTPut:STATe {state:b}')

    def voltage_arb(self, arb):
        """."""

        def upload(data, dwell):
            self.write(':SOURce:CURRent:MODE %s' % ('FIXed'))
            self.write(':SOURce:VOLTage:MODE %s' % ('ARB'))

            # self.query(':SOURce:ARB:FUNCtion:TYPE?')
            self.write(':SOURce:ARB:FUNCtion:TYPE %s' % ('VOLTage'))

            self.write(':FORMat:BORDer %s' % ('SWAP'))
            self.write(':FORMat:DATA %s' % ('REAL'))
            self.write_binary_values(
                ':SOURce:ARB:VOLTage:CDWell:LEVel ',
                data,
                datatype='f',
                is_big_endian=False,
            )

            self.write(':TRIGger:ARB:SOURce %s' % ('IMMediate'))
            self.write(':SOURce:ARB:VOLTage:CDWell:DWELl %G' % (dwell))
            # inst.write(':SOURce:ARB:VOLTage:CDWell:DWELl %G' % (0.00005))

            '''if self.query_binary_values(
                ':SOURce:ARB:VOLTage:CDWell:LEVel?', 'f', False
            ) == data:
                return True
            '''

        # generator = FunctionName(inst)
        # Inital call of next(generator) runs the init/setup, when next is called the first time
        # RST ?
        upload(arb['Voltage'].values, arb.attrs['Sample Rate'])
        
        # ready idle
        
        
        
        # Using next(generator) and subsequent calls to next(generator) yields a measurement

        # A subsequent call to the generator.send() allows input of infomation to the generator
        # The input of the generator.send(input) will be the result of the yield statement
        # x in this case
        
        state = None  # Using None allows you to not have to use generator.send(None) when you don't have data to input
        # This also allows is None to be used as a flow control
        state = yield state
        self.inst.timeout = int(len(arb['Voltage'].values) * arb.attrs['Sample Rate'] * 1000 * 1.5)
        while state is None:
            self.write(':INITiate:TRANsient')
            self.write(':TRIGger:TRANsient:IMMediate')
            state = yield float(self.query_bool('*OPC?'))
            # print(state)

        # When x is set to anything other than None, and the while loop finishes in that state this (↓) will be reached
        # self.inst.write('T0')  # Free run
        yield False
        
'''
def voltage_arb_load(self, arb, dwell=4*10.24e-6):

       

    def voltage_arb_trigger(self):
        self.write(':INITiate:TRANsient')
        sleep(0.2)
        self.write(':TRIGger:TRANsient:IMMediate')

    def voltage_arb_post_load(self):
        # self.write(f':SOURce:CURRent:LIMit:POSitive:IMMediate:AMPLitude MAXimum')
        self.write(f':SOURce:CURRent:LIMit:POSitive:IMMediate:AMPLitude MAXimum')
        # self.query_ascii_values(':OUTPut:RELay:LOCK:STATe?')
        self.write(f':OUTPut:RELay:LOCK:STATe {True:b}')
        

        self.query(':SOURce:ARB:TERMinate:LAST?')
        self.write(f':SOURce:ARB:TERMinate:LAST {False:b}')
        # False is state before arb
        # True is last value of arb

    def voltage_arb_abort(self):
        self.write(':ABORt:TRANsient')
        self.write(f':OUTPut:RELay:LOCK:STATe {False:b}')
        self.write(f':OUTPut:STATe {False:b}')
'''


'''

Using the ramp shapes and equation shown in the Keysight video for a 12V system you obtain: 
Python\Pulse2B.html
Should also be able to do Pulse 4
Python\Pulse4 from ISO 7637-2 2004 Figure 10.html

[SOURce:]ARB:VOLTage:CDWell time
dwell time In sec, rounded to nearest 0.00001024 s
== 0.01024 ms
Upload samples [SOURce:]ARB:VOLTage:CDWell[:LEVel] ARRAY
'''