#!/usr/bin/env python3
import time
import logging


class IEEE488(object):
    """IEEE 488 functions."""

    @property
    def CLS(self):
        """*CLS - Clear status."""
        self.write("*CLS")

    @property
    def ESE(self, value):
        """*ESE <enable_value> - Event status enable."""
        self.write("*ESE {}".format(value))

    @property
    def ESR(self):
        """*ESR? - Event status register query."""
        return(self.query("*ESR?"))

    @property
    def IDN(self):
        """*IDN? - Instrument identification."""
        return(self.query("*IDN?"))

    @property
    def OPC(self):
        """*OPC? - Wait for current operation to complete."""
        return(self.query("*OPC?"))

    @OPC.setter
    def OPC(self, value):
        """*OPC - Set operation complete bit."""
        self.write("*OPC {}".format(value))

    @property
    def OPT(self):
        """*OPT? - Show installed options."""
        return(self.query("*OPT?").split(','))

    @property
    def RCL(self, value=0):
        """*RCL {0|1|2|3|4} - Recall instrument state."""
        return(self.write("*RCL {}".format(value)))

    @property
    def RST(self):
        """*RST - Reset instrument to factory defaults."""
        return(self.write("*RST"))



'''

*PSC {0|1} - Power-on status clear


*SAV {0|1|2|3|4} - Save instrument state

*SRE <enable_value> - Service request enable (enable bits in enable register of Status Byte Register group

*STB? - Read status byte

*TRG - Trigger command

*TST? - Self-test

*WAI - Wait for all pending operations to complete
'''
