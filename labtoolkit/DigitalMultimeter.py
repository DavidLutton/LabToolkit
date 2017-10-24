#!/usr/bin/env python3
"""."""
import time
import logging
# import pint

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class DigitalMultimeter(GenericInstrument):
    """Parent class for DigitalMultimeters."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)


class HP3457A(DigitalMultimeter):
    """HP 3457A.

    .. figure::  images/DigitalMultimeter/HP3457A.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('HEWLETT-PACKARD,???,')

        # self.siggen.write("*CLS")  # clear error status
    def state(self):
        """."""
        print("Function: {}".format(self.function))
        print("Range: {}".format(self.range))
        print("Trigger: {}".format(self.trigger))


class HP3478A(DigitalMultimeter):
    """HP 3478A.

    .. figure::  images/DigitalMultimeter/HP3478A.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('HEWLETT-PACKARD,???,')

        # self.siggen.write("*CLS")  # clear error status
    def state(self):
        """."""
        print("Function: {}".format(self.function))
        print("Range: {}".format(self.range))
        print("Trigger: {}".format(self.trigger))


class HP34401A(DigitalMultimeter):
    """HP 34401A.

    .. figure::  images/DigitalMultimeter/HP34401A.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('HEWLETT-PACKARD,???,')

        # self.siggen.write("*CLS")  # clear error status
    def state(self):
        """."""
        print("Function: {}".format(self.function))
        print("Range: {}".format(self.range))
        print("Trigger: {}".format(self.trigger))

    @property
    def trigger(self):
        """."""
        return(self.query("TRIGger:SOURce?"))

    @trigger.setter
    def trigger(self, trigger="IMMediate"):  # BUS|IMMediate|EXTernal
        self.write("TRIGger:SOURce {}".format(trigger))

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
        self.write('SENSe:FUNCtion "{}"'.format(function))

    @property
    def range(self):
        """."""
        return(self.query("RANGe?"))

    @range.setter
    def range(self, range="MAXimum"):  # <range >|MINimum|MAXimum
        self.write("RANGe {}".format(range))

    @property
    def rangeauto(self):
        """."""
        return(self.query("RANGe:AUTO?"))

    @rangeauto.setter
    def rangeauto(self, rangeauto=True):
        self.write("RANGe {}".format(rangeauto))

    @property
    def rangeauto(self):
        """."""
        return(self.query("INPut:IMPedance:AUTO?"))

    @rangeauto.setter
    def rangeauto(self, impedanceauto=False):
        self.write("INPut:IMPedance:AUTO {}".format(impedanceauto))

    @property
    def reading(self):
        """."""
        return(float(self.query('READ?')))


class TZ4000(DigitalMultimeter):
    """TZ4000.

    .. figure::  images/DigitalMultimeter/TZ4000.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))


class Keithley2015(DigitalMultimeter):
    """."""

    @property
    def reading(self):
        """."""
        inst.query(float(':FETCh?'))


class Fluke8846A(DigitalMultimeter, IEEE488):
    """.

    .. figure::  images/DigitalMultimeter/Fluke8846A.jpg
    """

    def preset(self):
        """."""
        self.CLS
        self.write('system:remote')
        self.write('disp:off')
        # self.write('conf:volt:dc:nplc 60')

    @property
    def reading(self):
        """."""
        inst.query(float(':FETCh?'))


class Fluke8845A(Fluke8846A):
    """."""


REGISTER = {
    'HEWLETT-PACKARD,34401A': HP34401A,
    'HEWLETT-PACKARD,3457A': HP3457A,
    'HEWLETT-PACKARD,3478A': HP3478A,
    'TZ4000': TZ4000,
    'Keithley, 2015,': Keithley2015,
    'Fluke, 8845,': Fluke8845A,
    'Fluke, 8846,': Fluke8846A,

}

'''
http://www.eevblog.com/forum/metrology/raspberry-pi23-logging-platform-for-voltnuts/350/
Support HP 34401A/3446xA
Support HP 3458A (can test this)
Support Keithley 2000
Support Keithley 2001/2002 (can test this with both 2001 and 2002)
Keithley 2510 TEC SMU
Keithley 2001, 2002, 2400, 2510, 182, HP 3458, Wavetek 4920/4920M.
LAN for Keithley DMM7510, Tek DMM4050/Fluke 8846A and Keysight 3446xA/34470A.
Rigol DM3068
3458A

Keysight 34461A, Rigol DM3068 over LAN.

Agilent E5810A
3458A,K2001,K2002
Future phases  3441xA/34401A/3446xA
Keysight 34461A over either LAN or USB, please.
I have an HP3456A and Agilent HPIB to USB interface on the way. Also have RP3.
I also have an 3456 on the way and a Agilent 82357B clone, 2xBME280 on the way, all to join the K2000 and the 3457.
So for me would be great in the 3456/7 could be add to the list.
I have a recent 3458A (Firm. Rev. 9.2), 34470A and Keithley 2000
If I remember K2001 and K2002 have 3458A GPIB compatibility mode ... so supporting 3458A means also K2001 and K2002.
HP3478A
Keithley 2000
DP832
TEK TDS5052B
HP3245A
FLUKE 87V
HP33120A
34461A - Agilent
34410A - Agilent
DMM7510 - Keithley
2450 SMU - Keithley
DM3068 - Rigol
KEITHLEY INSTRUMENTS INC.,MODEL 6517B,1234567,A13/700x
Agilent Technologies,34411A,MY12345678,2.41-2.40-0.09-46-09
KEITHLEY INSTRUMENTS INC.,MODEL 2001M,1234567,B17  /A02
HM8012
HM8012 benchtop multimeter with RS232, a RK8511 DC electronic load with RS232 and a Siglent SPD3303D power supply with an USB po
BME280
Rigol DM3068
KEITHLEY INSTRUMENTS INC.,MODEL 2015,1043877,B15  /A02
SPD3303D power supply.
Siglent Technologies,SPD3303,SPD00002130137,1.01.01.01.05,V1.1
Rigol DM3068
SPD3303
KEITHLEY INSTRUMENTS INC.,MODEL 2015,1043877,B15  /A02
Agilent Technologies,34411A,MY12345678,2.41-2.40-0.09-46-09
Siglent Technologies,SPD3303,SPD00002130137,1.01.01.01.05,V1.1

Rigol DM3068
Keysight U1272a
inst_3458A.write("PRESET NORM")                     # commands the 3458a to preset state
inst_3458A.write("OFORMAT ASCII")
inst_3458A.write("NPLC 100")                        # commands the 3458a to 100 number power line cycles
inst_3458A.write("NDIG 8")                          # commands the 3458a to display 8.5 digits of resolution
inst_3458A.write("TARM HOLD")
inst_3458A.write("TRIG AUTO")
inst_3458A.write("AZERO ON")
inst_3458A.write("NRDGS 1,AUTO")
inst_3458A.write("MEM OFF")
inst_3458A.write("END ALWAYS")
inst_3458A.write("DELAY 0")
inst_3458A.write("LFILTER ON")
'''
# benchview supported 34401A, 34405A, 34410A, 34411A, 34420A, 34450A, 34460A, 34461A, 34465A, 34470A
