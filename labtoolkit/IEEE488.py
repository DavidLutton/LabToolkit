from .GenericInstrument import GenericInstrument


class IEEE488(GenericInstrument):
    """IEEE 488 functions."""

    def __repr__(self):
        # IDN = ', '.join(self.IDN.replace(', ', ',').split(',')[0:3])  # Make, Model, Serial
        # return f"{type(self).__name__} on {self.inst.resource_name} with {IDN}"
        try:
            self._IDN_
        except AttributeError:
            self._IDN_ = ', '.join(self.IDN.replace(', ', ',').split(',')[0:3])  # Make, Model, Serial
        finally:
            return f'{type(self).__name__} on {self.inst.resource_name} with {self._IDN_}'

    @property
    def CLS(self):
        r"""\*CLS - Clear status."""
        self.write("*CLS")

    def ESE(self, value):
        r"""\*ESE <enable_value> - Event status enable."""
        self.write(f"*ESE {value}")

    @property
    def ESR(self):
        r"""\*ESR? - Event status register query."""
        return self.query("*ESR?")

    @property
    def IDN(self):
        r"""\*IDN? - Instrument identification."""
        return self.query("*IDN?")

    @property
    def OPC(self):
        r"""\*OPC? - Wait for current operation to complete."""
        return self.query("*OPC?")

    @OPC.setter
    def OPC(self, value):
        r"""\*OPC - Set operation complete bit."""
        self.write(f"*OPC {value}")

    @property
    def OPT(self):
        r"""\*OPT? - Show installed options."""
        return self.query("*OPT?").split(',')

    def RCL(self, value=0):
        r"""\*RCL {0|1|2|3|4} - Recall instrument state."""
        return self.write(f"*RCL {value}")

    def RST(self):
        r"""\*RST - Reset instrument."""
        return self.write("*RST") 

    @property
    def WAI(self):
        r"""\*WAI - Wait for all pending operations to complete."""
        return self.query("*WAI") 

    @property
    def PSC(self, boolean):
        r"""\*PSC {0|1} - Power-on status clear."""
        return self.query("*PSC".format(boolean))

    @property
    def STB(self):
        r"""\*STB? - Read status byte."""
        return self.query("*STB?")

    @property
    def TRG(self):
        r"""\*TRG - Trigger command."""
        return self.write("*TRG") 

    @property
    def TST(self):
        r"""\*TST? - Self-test."""
        return self.query("*TST?")

    def SAV(self, index):
        r"""\*SAV {0|1|2|3|4} - Save instrument state."""
        return self.query(f"*SAV{index}")

    def SRE(self, value):
        r"""\*SRE <enable_value> - Service request enable (enable bits in enable register of Status Byte Register group."""
        return self.write(f"*SRE{value}")