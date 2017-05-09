#!/usr/bin/env python3
import time
import logging
import pint

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class DigitalMultimeter(GenericInstrument):
    """Parent class for DigitalMultimeters."""

    def __init__(self, instrument):
        super().__init__(instrument)


class HP3457A(DigitalMultimeter):
    """HP 3457A.

    .. figure::  images/DigitalMultimeter/HP3457A.jpg
    """

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('HEWLETT-PACKARD,???,')

        # self.siggen.write("*CLS")  # clear error status
    def state(self):
        print("Function: {}".format(self.function))
        print("Range: {}".format(self.range))
        print("Trigger: {}".format(self.trigger))


class HP3478A(DigitalMultimeter):
    """HP 3478A.

    .. figure::  images/DigitalMultimeter/HP3478A.jpg
    """

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('HEWLETT-PACKARD,???,')

        # self.siggen.write("*CLS")  # clear error status
    def state(self):
        print("Function: {}".format(self.function))
        print("Range: {}".format(self.range))
        print("Trigger: {}".format(self.trigger))


class HP34401A(DigitalMultimeter):
    """HP 34401A.

    .. figure::  images/DigitalMultimeter/HP34401A.jpg
   """

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('HEWLETT-PACKARD,???,')

        # self.siggen.write("*CLS")  # clear error status
    def state(self):
        print("Function: {}".format(self.function))
        print("Range: {}".format(self.range))
        print("Trigger: {}".format(self.trigger))

    @property
    def trigger(self):
        return(self.query("TRIGger:SOURce?"))

    @trigger.setter
    def trigger(self, trigger="IMMediate"):  # BUS|IMMediate|EXTernal
        self.write("TRIGger:SOURce {}".format(trigger))

    @property
    def function(self):
        return(self.query("FUNCtion?"))

    @function.setter
    def function(self, function="VOLTage:DC"):
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
        self.write("FUNCtion {}".format(function))

    @property
    def range(self):
        return(self.query("RANGe?"))

    @range.setter
    def range(self, range="MAXimum"):  # <range >|MINimum|MAXimum
        self.write("RANGe {}".format(range))

    @property
    def rangeauto(self):
        return(self.query("RANGe:AUTO?"))

    @rangeauto.setter
    def rangeauto(self, rangeauto=True):
        self.write("RANGe {}".format(rangeauto))

    @property
    def rangeauto(self):
        return(self.query("INPut:IMPedance:AUTO?"))

    @rangeauto.setter
    def rangeauto(self, impedanceauto=False):
        self.write("INPut:IMPedance:AUTO {}".format(impedanceauto))

    @property
    def reading(self):
        return(float(self.query('READ?')))


register = {
    "IDN": HP34401A,
}
