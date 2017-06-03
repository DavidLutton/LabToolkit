#!/usr/bin/env python3
import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

try:
    from Instrument.GenericInstrument import GenericInstrument
    from Instrument.IEEE488 import IEEE488
    from Instrument.SCPI import SCPI

except ImportError:
    from GenericInstrument import GenericInstrument
    from IEEE488 import IEEE488
    from SCPI import SCPI


class PowerMeter(GenericInstrument):
    """."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

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

        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith("HEWLETT-PACKARD,E4418B,") or self.IDN.startswith('Agilent Technologies,E4418B,')
        # self.write('*CLS')

        # self.__preset__()

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def status(self):
        """."""
        print('CF:  {}'.format(self.cfactor))
        print('CF:  {}HZ'.format(self.frequency))
        print('RCF:  {}'.format(self.rcfactor))
        print('Reference:  {}'.format(self.reference))
        print('Offset:  {}dB {}'.format(self.offset, self.offseten))
        print('Units:  {}'.format(self.units))
        print('Resolution:  {}'.format(self.resolution))

    @property
    def frequency(self):
        """Frequency used for correction factor lookup."""
        return(float(self.query(":SENSe1:FREQuency:CW?")))

    @frequency.setter
    def frequency(self, freq):
        # SENSe1:FREQuency:CW 26.5GHz
        self.write(":SENSe1:FREQuency:CW {}".format(freq))

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
        self.write(':OUTPut:ROSCillator:STATe {}'.format(int(state)))

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
        self.write('CALibration1:RCFactor {}'.format(factor))

    @property
    def offset(self):
        """Offset input attenuation."""
        return(float(self.query('CALCulate1:GAIN:MAGNitude?')))

    @offset.setter
    def offset(self, offset=0):
        self.write('CALCulate1:GAIN:MAGNitude {}'.format(offset))

    @property
    def offseten(self):
        """Offset state."""
        return(bool(int(self.query('CALCulate1:GAIN:STATe?'))))

    @offseten.setter
    def offseten(self, offset=False):
        self.write('CALCulate1:GAIN:STATe {}'.format(int(offset)))

    @property
    def cfactor(self):
        """Correction factor for readings (84nn series heads)."""
        return(float(self.query(":SENSe1:CORRection:CFACtor?")))

    @cfactor.setter
    def cfactor(self, factor):
        self.write(":SENSe1:CORRection:CFACtor {}".format(factor))

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
        self.write('DISPlay:WINDow1:RESolution {}'.format(resolution))


class HP437B(PowerMeter, IEEE488):
    """HP 437B.

    .. figure::  images/PowerMeter/HP437B.jpg
    """

    def __init__(self, instrument, logger=None):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.log.info('Creating an instance of\t' + str(__class__))

        assert self.IDN.startswith('HEWLETT-PACKARD,437B,')
        self.__preset__()

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __preset__(self):
        """."""
        # self.message("")
        self.log.info("Get   {} to known state".format(self.instrument.resource_name))
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
    '''DD display disable
        DE display enable
        DF display enable
        DU display user message
    '''
    # print(dispatch[key])  # PowerMeter[0].key("Left")
    # self.instrument.write(dispatch[key])

    def zero(self):
        """."""
        self.write("CS;ZE")

    def calibrate(self, factor=100.0):
        """."""
        self.write("CS;CL{}EN".format(factor))

    def correctionfactor(self, factor=100.0):
        """."""
        self.write("KB{}EN".format(factor))  # KB enter measurement cal factor

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
}
