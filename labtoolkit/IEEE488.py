#!/usr/bin/env python3
"""."""
import time
import logging


class IEEE488(object):
    """IEEE 488 functions."""

    @property
    def CLS(self):
        r"""\*CLS - Clear status."""
        self.write("*CLS")

    @property
    def ESE(self, value):
        r"""\*ESE <enable_value> - Event status enable."""
        self.write(f"*ESE {value}")

    @property
    def ESR(self):
        r"""\*ESR? - Event status register query."""
        return(self.query("*ESR?"))

    @property
    def IDN(self):
        r"""\*IDN? - Instrument identification."""
        return(self.query("*IDN?"))

    @property
    def OPC(self):
        r"""\*OPC? - Wait for current operation to complete."""
        return(self.query("*OPC?"))

    @OPC.setter
    def OPC(self, value):
        r"""\*OPC - Set operation complete bit."""
        self.write(f"*OPC {value}")

    @property
    def OPT(self):
        r"""\*OPT? - Show installed options."""
        return(self.query("*OPT?").split(','))

    @property
    def RCL(self, value=0):
        r"""\*RCL {0|1|2|3|4} - Recall instrument state."""
        return(self.write(f"*RCL {value}"))

    @property
    def RST(self):
        r"""\*RST - Reset instrument to factory defaults."""
        return(self.write("*RST"))

    @property
    def WAI(self):
        r"""\*WAI - Wait for all pending operations to complete."""
        return(self.query("*WAI"))

    @property
    def PSC(self, boolean):
        r"""\*PSC {0|1} - Power-on status clear."""
        return(self.query("*PSC".format(boolean)))

    @property
    def STB(self):
        r"""\*STB? - Read status byte."""
        return(self.query("*STB?"))

    @property
    def TRG(self):
        r"""\*TRG - Trigger command."""
        return(self.write("*TRG"))

    @property
    def TST(self):
        r"""\*TST? - Self-test."""
        return(self.query("*TST?"))

    @property
    def SAV(self, interger):
        r"""\*SAV {0|1|2|3|4} - Save instrument state."""
        return(self.query("*SAV".format(interger)))

    @property
    def SRE(self, interger):
        r"""\*SRE <enable_value> - Service request enable (enable bits in enable register of Status Byte Register group."""
        return(self.query("*SRE".format(interger)))
