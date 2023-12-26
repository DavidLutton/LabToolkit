from ..IEEE488 import IEEE488
from ..SCPI import SCPI

class HP34401A(IEEE488, SCPI):
    """HP 34401A.

    .. figure::  images/DigitalMultimeter/HP34401A.jpg
    """
    # self.siggen.write("*CLS")  # clear error status


    def state(self):
        """."""
        print(f"Function: {self.function}")
        print(f"Range: {self.range}")
        print(f"Trigger: {self.trigger}")

    @property
    def trigger(self):
        """."""
        return(self.query("TRIGger:SOURce?"))

    @trigger.setter
    def trigger(self, trigger="IMMediate"):  # BUS|IMMediate|EXTernal
        self.write(f"TRIGger:SOURce {trigger}")

    @property
    def function(self):
        """."""
        return(self.query("FUNCtion?"))

    @function.setter
    def function(self, function="VOLTage:DC"):
        """."""
        '''
        VOLTage:DC
        VOLTage:DC:RATio
        VOLTage:AC
        CURRent:DC
        CURRent:AC
        RESistance ( 2-wire ohms )
        FRESistance ( 4-wire ohms )
        FREQuency
        PERiod
        CONTinuity
        DIODe
        '''
        self.write(f'SENSe:FUNCtion "{function}"')

    @property
    def range(self):
        """."""
        return(self.query("RANGe?"))

    @range.setter
    def range(self, range="MAXimum"):  # <range >|MINimum|MAXimum
        self.write(f"RANGe {range}")

    @property
    def rangeauto(self):
        """."""
        return(self.query("RANGe:AUTO?"))

    @rangeauto.setter
    def rangeauto(self, rangeauto=True):
        self.write(f"RANGe {rangeauto}")

    @property
    def rangeauto(self):
        """."""
        return(self.query("INPut:IMPedance:AUTO?"))

    @rangeauto.setter
    def rangeauto(self, impedanceauto=False):
        self.write(f"INPut:IMPedance:AUTO {impedanceauto}")

    @property
    def reading(self):
        """."""
        return self.query_float('READ?')