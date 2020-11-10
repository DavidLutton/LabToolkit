from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class AgilentE4418B(IEEE488, SCPI):
    """Agilent E4418B.

    .. figure::  images/PowerMeter/AgilentE4418B.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        # self.__preset__()

    def status(self):
        """."""
        # print('CF:  {}'.format(self.cfactor))
        print('CF:         {} Hz'.format(self.frequency))
        # print('RCF:  {}'.format(self.rcfactor))
        print('Reference:  {}'.format(self.reference))
        print('Offset:     {} dB {}'.format(self.offset, self.offseten))
        print('Units:      {}'.format(self.units))
        print('Resolution: {}'.format(self.resolution))

    @property
    def frequency(self):
        """Frequency used for correction factor lookup."""
        return(float(self.query(":SENSe1:FREQuency:CW?")))

    @frequency.setter
    def frequency(self, freq):
        # SENSe1:FREQuency:CW 26.5GHz
        self.write(":SENSe1:FREQuency:CW {}".format(freq))

    @property
    def amplitude(self):
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
    def calfactor(self):
        """Correction factor for readings (84nn series heads)."""
        return(float(self.query(":SENSe1:CORRection:CFACtor?")))

    @calfactor.setter
    def calfactor(self, factor):
        self.write(":SENSe1:CORRection:CFACtor {}".format(factor))

    @property
    def units(self):
        """Readback units."""
        return(self.query('UNIT:POWer?'))

    @units.setter
    def units(self, unit='DBM'):  # W
        self.write(f'UNIT:POWer {unit}')

    @property
    def resolution(self):
        """."""
        return self.query('DISPlay:WINDow1:RESolution?')

    @resolution.setter
    def resolution(self, resolution='4'):
        self.write('DISPlay:WINDow1:RESolution {}'.format(resolution))

    @property
    def cfactor(self):
        """Correction factor for readings (84nn series heads)."""
        return(float(self.query(":SENSe1:CORRection:CFACtor?")))

    @cfactor.setter
    def cfactor(self, factor):
        self.write(f":SENSe1:CORRection:CFACtor {factor}")
