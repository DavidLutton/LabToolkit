#!/usr/bin/env python3
"""."""

import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class PowerMeter(GenericInstrument):
    """."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def correctionfactorinterpolateload(self, listoffrequencys, listofffactors):
        """."""
        assert len(listoffrequencys) == len(listofffactors)
        if len(listoffrequencys) == len(listofffactors):
            self.correctionfactorsx = listoffrequencys
            self.correctionfactorsy = listofffactors

    def correctionfactorinterpolate(self, frequencyofwantedfactor):
        """."""
        return (UnivariateSpline(self.correctionfactorsx, self.correctionfactorsy, k=5, s=.05))(frequencyofwantedfactor)


class AgilentE4418B(PowerMeter, SCPI, IEEE488):
    """Agilent E4418B.

    .. figure::  images/PowerMeter/AgilentE4418B.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith("HEWLETT-PACKARD,E4418B,") or self.IDN.startswith('Agilent Technologies,E4418B,')
        # self.write('*CLS')

        # self.__preset__()

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def status(self):
        """."""
        print(f'CF:  {self.cfactor}')
        print(f'CF:  {self.frequency}HZ')
        print(f'RCF:  {self.rcfactor}')
        print(f'Reference:  {self.reference}')
        print(f'Offset:  {self.offset}dB {self.offseten}')
        print(f'Units:  {self.units}')
        print(f'Resolution:  {self.resolution}')

    @property
    def frequency(self):
        """Frequency used for correction factor lookup."""
        return(float(self.query(":SENSe1:FREQuency:CW?")))

    @frequency.setter
    def frequency(self, freq):
        # SENSe1:FREQuency:CW 26.5GHz
        self.write(f":SENSe1:FREQuency:CW {freq}")

    @property
    def measurement(self):
        """Get reading of power level."""
        return(float(self.query(":FETCh1:SCALar:POWer:AC?")))

    @property
    def reference(self):
        """Reference state."""
        return(bool(int(self.query(":OUTPut:ROSCillator:STATe?"))))

    @reference.setter
    def reference(self, state):
        self.write(f':OUTPut:ROSCillator:STATe {int(state)}')

    @property
    def zero(self):
        """Zero the power head."""
        self.write('CALibration1:ZERO:AUTO ONCE')

    @property
    def calibrate(self):
        """Calibrate against a power source."""
        self.write('CALibration1:AUTO ONCE')

    @property
    def rcfactor(self):
        """Correction factor for calibration (84nn series heads)."""
        return(float(self.query('CALibration1:RCFactor?')))

    @rcfactor.setter
    def rcfactor(self, factor=100):
        self.write(f'CALibration1:RCFactor {factor}')

    @property
    def offset(self):
        """Offset input attenuation."""
        return(float(self.query('CALCulate1:GAIN:MAGNitude?')))

    @offset.setter
    def offset(self, offset=0):
        self.write(f'CALCulate1:GAIN:MAGNitude {offset}')

    @property
    def offseten(self):
        """Offset state."""
        return(bool(int(self.query('CALCulate1:GAIN:STATe?'))))

    @offseten.setter
    def offseten(self, offset=False):
        self.write(f'CALCulate1:GAIN:STATe {int(offset)}')

    @property
    def cfactor(self):
        """Correction factor for readings (84nn series heads)."""
        return(float(self.query(":SENSe1:CORRection:CFACtor?")))

    @cfactor.setter
    def cfactor(self, factor):
        self.write(f":SENSe1:CORRection:CFACtor {factor}")

    @property
    def units(self):
        """Readback units."""
        return(self.query('UNIT:POWer?'))

    @units.setter
    def units(self, unit='DBM'):  # W
        self.write('UNIT:POWer '.format(unit))

    @property
    def resolution(self):
        """."""
        return(self.query('DISPlay:WINDow1:RESolution?'))

    @resolution.setter
    def resolution(self, resolution='4'):
        self.write(f'DISPlay:WINDow1:RESolution {resolution}')


class HP437B(PowerMeter, IEEE488):
    """HP 437B.

    .. figure::  images/PowerMeter/HP437B.jpg
    """

    def __init__(self, instrument, logger=None):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith('HEWLETT-PACKARD,437B,')
        # self.__preset__()

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def preset(self):
        """."""
        # self.message("")
        self.log.info(f"Get {self.engineering_project.resource_name} to known state")
        self.correctionfactor(100.0)
        self.rangeauto()
        self.unitslog()  # Log units dBM/dB
        # self.rangehold(self):  # RH Range hold
        # self.rangemanual(self, ranger)
        # self.write("RM{}".format(ranger))

        # self.lin():  # Linear units (Watts/%)
        self.zero()

    def discover(self):
        """."""
        decodeTHISARRAY = self.query("LP2")  # TODO

    def measure(self):
        """."""
        measure = float(self.query("?"))
        if measure is not 9e40 and measure is not 9.0036e40:
            return(measure)

    def message(self, message=None):
        """."""
        if message is not None and len(message) <= 12:
            self.write("DU" + message.rjust(12))
        else:
            self.write("DE")

    def displayread(self):
        """."""
        pass  # OD

    def key(self, key):
        """."""
        dispatch = {
            "Up": "UP",  # Up arrow key
            "Down": "DN",  # Down arrow key
            "Left": "LT",  # Left arrow key
            "Right": "RT",  # Right arrow key
            "Enter": "EN",  # Enter key
            "Exit": "EX",  # exit function
            "Preset": "PR",
            "Special": "SP",
            "Zero": "ZE",
        }
        # print(dispatch[key])  # PowerMeter[0].key("Left")
        self.write(dispatch[key])

    # def display(self, key):
    # DD display disable
    #    DE display enable
    #    DF display enable
    #    DU display user message

    # print(dispatch[key])  # PowerMeter[0].key("Left")
    # self.engineering_project.write(dispatch[key])

    def zero(self):
        """."""
        self.write("CS;ZE")

    def calibrate(self, factor=100.0):
        """."""
        self.write(f"CS;CL{factor}EN")

    def correctionfactor(self, factor=100.0):
        """."""
        self.write(f"KB{factor}EN")  # KB enter measurement cal factor

    def statusmessage(self):
        """."""
        status = self.query("SM")
        #  $Message[5,6] = “06” Wait until zero completes (06 means zeroing)
        #  $Message[5,6] = ! Wait until cal completes (08 means calibrating
        return(status)

    def rangeauto(self):
        """."""
        self.write("RA")

    def rangehold(self):  # RH Range hold
        """."""
        self.write("RH")

    def rangemanual(self, range):
        """."""
        self.write("RM")

    def lin(self):  # Linear units (Watts/%)
        """."""
        self.write("LN")
        self.units = "W"

    def unitslog(self):  # Log units dBM/dB
        """."""
        self.write("LG")
        self.units = "dBm"


'''
*CLS Clear all status registers
CS clear the status byte
CT clear sensor type
DA All display segments on
DC0 Duty cycle off
DC1 Duty cycle on

DY enter duty cycle
ERR? Device error query
*ESR? Event status register query
*ESE Set event status register mask
*ESE? event status register mask query
ET Edit sensor table
FA automatic filter selection
FH filter hold
FM Manual filter selection
FR enter measurement frequency
GT0 ignore GET bus command
GT1 Trigger immediate response to get
GT2 Trigger with delay response to get
GZ Gigaherz
HZ Hertz

KZ kilohertz
LH enter high Limit
LL Enter low Limit
LM0 disable limits checking
LM1 enable limits checking

LP2 learn mode
MZ megahertz
OC0 reference oscillator off
OC1 reference oscillator on
OD output display
OF0 offset off
OF1 offset on
OS offset Value
PCT Percent

RA Auto range
RC recall instrument configuration
RE Set display resolution
RF Enter sensor table reference alibration factor
RL0 exit from relative mode
RL1 Enter relative mode (take new reference)
RL2 Enter relative mode (use last reference)
RM Set measurement range
*RST reset
RV Read service request mask
SE Select sensor calibration table
SM  Status message
SN Enter sensor identification/serial number

*SRE Set the service request mask
*SRE? Service request mask query
ST Store (save) power meter configuration
*STB? Read status byte
TR0 trigger hold
TR1 trigger immediate
TR2 trigger with delay
*TST? self test query

@1 Prefix for status mask
@2 Learn mode prefix
% Percent
'''


class RohdeSchwarzNRVS(PowerMeter):
    """Rohde-Schwarz NRVS.

    .. figure::  images/PowerMeter/RohdeSchwarzNRVS.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    @property
    def measurement(self):
        """Get reading of power level."""
        vals = self.query('x3').strip().split(' ')
        unit = vals[0]
        value = float(vals[-1])
        # print('{} {}'.format(value, unit))
        return(value)


class RohdeSchwarzURV4(PowerMeter):
    """RohdeSchwarz URV 4.

    .. figure::  images/PowerMeter/RohdeSchwarzURV4.jpg
    """


class Bird4421(PowerMeter):
    """Bird 4421.

    .. figure::  images/PowerMeter/Bird4421.jpg
    """


REGISTER = {
    "HEWLETT-PACKARD,437B,": HP437B,
    "Agilent Technologies,E4418B,": AgilentE4418B,
    "HEWLETT-PACKARD,E4418B,": AgilentE4418B,
    # NVRS
    # R&S ???4
    # Bird 4421
    # Benchview Supported N1911A, N1912A, N1913A, N1914A, N8262A,
    # Benchview Supported U2000A, U2000B, U2000H, U2001A, U2001B, U2001H, U2002A, U2002H, U2004A, U2021XA, U2022XA, U2041XA, U2042XA, U2043XA, U2044XA, U2049XA LAN, U8481A, U8485A, U8487A, U8488A
}
