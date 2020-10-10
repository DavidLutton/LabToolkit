#!/usr/bin/env python3
"""."""

import time
import logging
# import pint

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class SignalGenerator(GenericInstrument):
    """."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.amplimit = 0

    def safe(self):
        """Make safe the SignalGenerator."""
        self.output = False
        self.amplitude = min(self.amps)
        # self.frequency = min(self.freqs)

    def state(self):
        """Report basic paramaters."""
        print(f"Amplitude: {self.amplitude}")
        print(f"Frequency: {self.frequency}")
        print(f"Output: {self.output}")

    def start(self, lvl=-50):
        """."""
        self.amplitude = lvl

    '''def ampsetter(self, targetlevel):
        if (self.amplitude - 10) <= targetlevel <= (self.amplitude + 3):
            self.amp(targetlevel)
        else:
            before = str(self.amplitude)  # self.log.warn("on " + self.IDN + " amp change limits, set" + str(self.amplitude))
            if (self.amplitude - 10) >= targetlevel:
                self.amp((self.amplitude - 10))
            if (self.amplitude + 3) <= targetlevel:
                self.amp((self.amplitude + 3))
            self.log.warn("on " + self.IDN + " amp change limits, set " + str(self.amplitude) + " from " + before)

    def freqsetter(self, freq):
        if self.frequency != freq:  # prevent resubmitting request to set the same frequency

            self.write(freq)
            self.frequency = freq
            time.sleep(.3)  # after retuneing wait time for settling
    '''


class amplitudelimiter(object):
    """Class to limit upper amplitude value applied to a SignalGenerator.

    Applied by decorator @amplitudelimiter
    """

    def __init__(self, f, *args, **kwargs):
        """If there are no decorator arguments, the function to be decorated is passed to the constructor."""
        # print(f)
        # print(*args)
        # print(**kwargs)
        # print("Inside __init__()")
        self.f = f

    def __call__(self, f, *args, **kwargs):
        """The __call__ method is not called until the decorated function is called."""
        # print(f)
        print(*args)
        # print(**kwargs)
        # print("Inside __call__()")
        setpoint = float(*args)
        if setpoint > f.amplimit:
            f.log.warn(f"Amplimit ({f.amplimit}) reached with setpoint ({setpoint}) on {f.instrument}")
        else:
            self.f(f, *args)
        # print("After self.f(*args)")


class SCPISignalGenerator(SignalGenerator, IEEE488, SCPI):
    """."""

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        # self.amps = [-140, 17]
        # self.freqs = [100e3, 3e9]
        # self.siggen.write("*CLS")  # clear error status
        # self.frequency = min(self.freqs)

    @property
    def frequency(self):
        """."""
        return(self.query("SOURce:FREQuency:CW?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"SOURce:FREQuency:CW {frequency:.0f} Hz")

    @property
    def amplitude(self):
        """."""
        return(self.query("SOURce:POWer:LEVel:AMPLitude?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"SOURce:POWer:LEVel:AMPLitude {amplitude:.2f} DBM")

    @property
    def output(self):
        """."""
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write(f"OUTPut:STATe {boolean:d}")


class HP8657A(SignalGenerator, IEEE488):
    """HP 8657A 100e3, 1040e6.

    .. figure::  images/SignalGenerator/HP8657A.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        assert self.IDN.startswith('HEWLETT-PACKARD,8657A,')
        # self.amps = [-111, 17]
        self.amps = [-143.5, 17]  # HP 8657A, 8657B
        # self.amps = [-127, 17]  # HP 8656B
        self.freqs = [100e3, 1040e6]

        # self.siggen.write("*CLS")  # clear error status

    @property
    def frequency(self):
        """."""
        return(self.query("FR?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"FR {frequency:.0f}Hz")

    @property
    def amplitude(self):
        """."""
        return(self.query("AP?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"AP {amplitude:.1f}DM")

    @property
    def output(self):
        """."""
        pass

    @output.setter
    def output(self, boolean=False):
        if boolean is False:
            self.write("R2")
        else:
            if boolean is True:
                self.write("R3")


class HP866nA(SignalGenerator, IEEE488):
    """HP 866nA."""
    def __init__(self, inst):
        self.inst = inst
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    @property
    def frequency(self):
        """."""
        return(self.query("FREQ:CW?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"FREQ:CW {frequency:.0f}Hz")

    @property
    def amplitude(self):
        """."""
        return(self.query("AMPL:OUT:LEV?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"AMPL:OUT:LEV {amplitude:.1f}DBM")

    @property
    def output(self):
        """."""
        if self.query("AMPL:OUT:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write(f"AMPL:OUT:STATe {boolean:d}")

    @property
    def frequency(self):
        return float(self.inst.query('FREQ:CW?'))

    @frequency.setter
    def frequency(self, frequency):
        self.inst.write(f'FREQ:CW {frequency:.2f} Hz')

    @property
    def power(self):
        return float(self.inst.query('AMPL:OUT:LEV?'))

    @power.setter
    def power(self, power):
        self.inst.write(f'AMPL:OUT:LEV {power:.1f} DBM')

    @property
    def output(self):
        """."""
        if self.inst.query('AMPL:OUT:STATe?') == '1':
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.inst.write(f'AMPL:OUT:STATe {boolean:d}')

    @property
    def fmdeviation(self):
        return self.inst.query('FM:DEViation?')

    @fmdeviation.setter
    def fmdeviation(self, deviation):
        self.inst.write(f'FM:DEViation {deviation} Hz')

    @property
    def fmfrequency(self):
        return self.inst.query('FM:FREQuency?')

    @fmfrequency.setter
    def fmfrequency(self, frequency):
        self.inst.write(f'FM:FREQuency {frequency} Hz')

    @property
    def fmmodulation(self):
        """."""
        if self.inst.query('FM:STATe?') == '1':
            return(True)
        else:
            return(False)

    @fmmodulation.setter
    def fmmodulation(self, boolean=False):
        self.inst.write(f'FM:STATe {boolean:d}')

    @property
    def amdepth(self):
        return self.inst.query('AM:DEPth?')

    @amdepth.setter
    def amdepth(self, depth):
        self.inst.write(f'AM:DEPth {depth}')

    @property
    def amfrequency(self):
        return self.inst.query('AM:FREQuency?')

    @amfrequency.setter
    def amfrequency(self, frequency):
        self.inst.write(f'AM:FREQuency {frequency} Hz')

    @property
    def ammodulation(self):
        """."""
        if self.inst.query('AM:STATe?') == '1':
            return(True)
        else:
            return(False)

    @ammodulation.setter
    def ammodulation(self, boolean=False):
        self.inst.write(f'AM:STATe {boolean:d}')

    @property
    def modulation(self):
        """."""
        if self.inst.query('MODulation:STATe?') == '1':
            return(True)
        else:
            return(False)

    @modulation.setter
    def modulation(self, boolean=False):
        self.inst.write(f'MODulation:STATe {boolean:d}')


class HP8664A(HP866nA):
    """HP 8664A 100e3, 3e9.

    .. figure::  images/SignalGenerator/HP8664A.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        assert self.IDN.startswith('HEWLETT_PACKARD,8664A,')
        self.amps = [-140, 17]
        self.freqs = [100e3, 3e9]


class HP8665B(HP866nA):
    """HP 8665B 100e3, 6e9.

    .. figure::  images/SignalGenerator/HP8665B.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        assert self.IDN.startswith('HEWLETT_PACKARD,8665B,')
        self.amps = [-140, 17]
        self.freqs = [100e3, 6e9]


class AgilentN5182A(SCPISignalGenerator):
    """Agilent N5182A 100e3, 6e9.

    .. figure::  images/SignalGenerator/AgilentN5182A.jpg
    """
    def __repr__(self):
        return(f"{__class__.__name__}, {self.instrument}")


class AgilentN5181A(SCPISignalGenerator):
    """Agilent N5181A 100e3, 3e9.

    .. figure::  images/SignalGenerator/AgilentN5181A.jpg
    """
    def __repr__(self):
        return(f"{__class__.__name__}, {self.instrument}")


class HPESG3000A(SignalGenerator, IEEE488):
    """Agilent E4422B 250e3, 3e9.

    .. figure::  images/SignalGenerator/HPESG3000A.jpg
    """


class AgilentE4422B(SignalGenerator, IEEE488):
    """Agilent E4422B 250e3, 4e9.

    .. figure::  images/SignalGenerator/AgilentE4422B.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        # assert self.IDN.startswith('Agilent Technologies, E4422B')

        self.amps = [-100, 16]
        self.freqs = [100e3, 4e9]
        # self.write("*CLS")  # clear error status

    @property
    def frequency(self):
        """."""
        return(self.query("FREQ?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"FREQ {frequency:.0f} Hz")

    @property
    def amplitude(self):
        """."""
        return(self.query("POWer?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"POWer {amplitude:.2f} dBm")

    @property
    def output(self):
        """."""
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write(f"OUTPut:STATe {boolean:d}")  # OUTP:STAT ON // OFF


class Anritsu_MG369NX():

    def __init__(self, inst):
        self.inst = inst
        self.inst.read_termination = '\r\n'
        self.inst.write_termination = '\n'
        self._fmin, self._fmax = float(self.inst.query('OFL')) * 1e6, float(self.inst.query('OFH')) * 1e6  # Min, Max Frequency
        self._options = [str(i) for i in self.inst.query('OO').split(',')]  # Options installed
        self._preset_()

    def _preset_(self):
        self.inst.write('CF0')  # select F0
        self.inst.write('L0')  # select L0

        self.inst.write('LOG')  # operate in dBm  / LIN in mV
        self.output = False
        self.inst.write('RO1')  # RF state at reset to off

        self.frequencymultiplier = 1
        self.leveloffset = 0
        self.inst.write('LO0')  # Level offset off

        self.inst.write('RL')
        '''
        # self.options = self.query("*OPT?").strip().split(',')

        # self.write("*CLS")  # clear error status
        # self.write("*CLS")  # clear error status
        # self.write('CF0')  # Set CW mode at F0, Opens F0 parameter.
        # self.write('CM0')  # Set CW mode at M0, Opens M0 parameter.
        # AL0
        # self.write('LOG')
        # self.query('SAF')  # Outputs the current instrument setup to the controller.
        # RCF Readies the MG369XB to receive a new instrument setup recalled from the controller
        self.query('OO')  # Returns the instrument option string to the controller
        self.write('RO1')  # Selects RF to be off at reset
        self.write('RL1')  # Release to Local
        '''

    @property
    def frequency(self):  # Responce is in MHz
        return round(float(self.inst.query('OF0')) * 1e6, 2)

    @frequency.setter
    def frequency(self, frequency):
        self.inst.write(f'F0{frequency:.2f}HZ')

    @property
    def frequencymultiplier(self):
        return float(self.inst.query('OFM'))  # Output Frequency Multiplier

    @frequencymultiplier.setter
    def frequencymultiplier(self, multiplier=1):
        self.inst.write(f"FRS{multiplier}TMS")  # Set Frequency Multiplier

    @property
    def level(self):
        return float(self.inst.query('OL0'))  # Output Level 0

    @level.setter
    def level(self, level):
        self.inst.write(f'L0{level:.2f}DM')

    @property
    def output(self):
        return NotImplemented  # ORF?

    @output.setter
    def output(self, boolean=False):
        self.inst.write(f'RF{boolean:d}')

    @property
    def leveloffset(self):
        return float(self.inst.query('OLO'))

    @leveloffset.setter
    def leveloffset(self, leveloffset):
        self.inst.write(f'LOS{leveloffset:.2f}DB')

    '''
    # 'F5 100 MZ ACW'  # Activate CW on open frequency param

    # AT0  # deselect coupling of ALC attenuator
    # AT1  # select coupling of ALC attenuator
    # ATT00 to ATT11 nn * 10 dB.

    # CS0  # Turns off CW Ramp

    # LVP  # set output -1dB of Peak power shy of

    # gen.query('OI')
    # gen.query('OVN')  # ROM Version

    # PS0  # Phase Offset Off
    # PSO{phase}DG

    # PU{n}
    # 0 dBm
    # 1 mV
    # 2 dBmV

    # TR0 , TR1  # when step attenuator is installed use 0 or 40dB of attenuation ~source match termination

        # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse
        LOS Opens the level offset
        parameter.
        +100dB to 100dB
        (logarithmic); +xxx mV to
        xxx mV (linear)
        DB (log)
        VT (linear

        # XL0
        Opens the L0 parameter.   Power level range of the
        MG369XB model
        DM (log)
        VT (linear)


    '''


class Wiltron6669A(SignalGenerator, IEEE488):
    """Wiltron 6669A 10e6, 40e9.

    .. figure::  images/SignalGenerator/Wiltron6669A.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        self.amps = [-20, 17]
        self.freqs = [10e6, 40e9]
        # self.siggen.write("*CLS")  # clear error status
        # self.frequency = min(self.freqs)

    @property
    def frequency(self):
        """."""
        return(self.query("OF0"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"F0{frequency:.2f}GH")

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"L0{amplitude:.2f}DM")

    '''@property
    def output(self):
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))
    '''


class Wiltron6672B(SignalGenerator, IEEE488):
    """Wiltron 6672B 40e9, 60e9.

    .. figure::  images/SignalGenerator/Wiltron6672B.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        self.amps = [-20, 17]
        self.freqs = [40e9, 60e9]
        # self.siggen.write("*CLS")  # clear error status
        # self.frequency = min(self.freqs)

    @property
    def frequency(self):
        """."""
        return(self.query("OF0"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"F0{frequency:.2f}GH")

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"L0{amplitude:.2f}DM")

    '''@property
    def output(self):
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))
    '''


class Wiltron360SS69(SignalGenerator, IEEE488):
    """Wiltron 360SS69 10e6, 40e9.

    .. figure::  images/SignalGenerator/Wiltron360SS69.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        self.amps = [-140, 17]
        self.freqs = [10e6, 40e9]
        # self.siggen.write("*CLS")  # clear error status
        # self.frequency = min(self.freqs)

    @property
    def frequency(self):
        """."""
        return(self.query("OF0"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"F0{frequency:.2f}GH")

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"L0{amplitude:.2f}DM")

    '''@property
    def output(self):
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))
    '''


class MarconiInstruments203N(SignalGenerator, IEEE488):
    """MarconiInstruments 203N 10e3, ...

    10 kHz to 1.35 GHz (2030)
    10 kHz to 2.7 GHz (2031)
    10 kHz to 5.4 GHz (2032)
    """
    def __init__(self, inst):
        self.inst = inst
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    '''

    print( inst.write('CFRQ:VALUE 1234.5678912MHZ') )

    MODE?
    MODE AM
    MODE FM
    MOD:ON
    MOD:OFF
    MOD?
    AM:DEPTH
    AM:INTF1
    AM:ON
    AM:OFF
    AM?
    INTF1  ,2,3,4,5,6
    INTF1:FREQ 1KHz
    INTF1:SIN
    INTF1?
    LF?
    LF:ON
    LF:OFF
    LFGF?
    LFGF:VALUE
    LFGF:SIN
    LFGF:TRI
    LFGL?
    LFGL:VALUE
    LFGL:UNITS DBM,DBV,DBMV,V,MV,UV
    SWEEP?
    BACKL:ON
    BACKL:OFF
    TIME?
    DATE?
    OPER? operating hours
    ELAPSED? hours since last reset
    ERROR?
    KLOCK
    KUNLOCK
    '''

    @property
    def frequency(self):
        """."""
        return float(self.query("CFRQ?").split(';')[0].split(' ')[1])  # ':CFRQ:VALUE 50000000.0;INC 1000.0'

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"CFRQ:VALUE {frequency:.1f}Hz")

    @property
    def amplitude(self):
        """."""
        return(self.query("RFLV?"))

    @amplitude.setter
    # @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"RFLV:VALUE {amplitude:.2f}DBM")

    @property
    def output(self):
        """."""
        print(self.query("RFLV?"))

    @output.setter
    def output(self, boolean=False):
        if boolean is True:
            self.write("RFLV:ON")
        else:
            self.write("RFLV:OFF")


class MarconiInstruments2030(MarconiInstruments203N):
    """MarconiInstruments 203N 10e3, ...

    10 kHz to 1.35 GHz (2030)
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        # assert self.IDN.startswith('Agilent Technologies, E4422B')

        self.amps = [-144, 13]
        self.freqs = [10e3, 1.35e9]
        # self.write("*CLS")  # clear error status


class MarconiInstruments2031(MarconiInstruments203N):
    """MarconiInstruments 203N 10e3, ...

    .. figure::  images/SignalGenerator/MarconiInstruments2031.jpg
    10 kHz to 2.7 GHz (2031)
    """

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        # assert self.IDN.startswith('Agilent Technologies, E4422B')

        self.amps = [-144, 13]
        self.freqs = [10e3, 2.7e9]
        # self.write("*CLS")  # clear error status


class MarconiInstruments2032(MarconiInstruments203N):
    """MarconiInstruments 203N 10e3, ...

    .. figure::  images/SignalGenerator/MarconiInstruments2032.jpg
    10 kHz to 5.4 GHz (2032)
    """

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        # assert self.IDN.startswith('Agilent Technologies, E4422B')

        self.amps = [-144, 13]
        self.freqs = [10e3, 5.4e9]
        # self.write("*CLS")  # clear error status


class KeysightN5173B(SCPISignalGenerator):
    """Keysight N5173B 9e3, 40e9.

    .. figure::  images/SignalGenerator/KeysightN5173B.jpg
    """


class AnritsuMG3710A(SCPISignalGenerator):
    """Anritsu MG3710A 100e3, 6e9.

    .. figure::  images/SignalGenerator/AnritsuMG3710A.jpg
    """


class RohdeSchwarzSHM52(SignalGenerator):
    """Rohde and Schwarz SHM, 100e3-2e9."""

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        self.amps = [-107, 17]
        self.freqs = [100e3, 2e9]

    @property
    def frequency(self):
        """."""
        return(self.query("RF?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"RF {frequency:.0f}HZ")

    @property
    def amplitude(self):
        """."""
        return(self.query("L:?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"LEV {amplitude:.1f}DBM")

    @property
    def output(self):
        """."""
        if self.query("L:?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        # LEV:OFF
        if boolean is False:
            # self.amplitude = min(self.amps)
            self.write("LEV:OFF")


class HP85645A(SignalGenerator, IEEE488, SCPI):
    """."""

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        self.amps = [-60, -2]
        self.freqs = [300e3, 26.5e9]

    '''
'HEWLETT-PACKARD,85645A,3407A00241,920427'  # E380

>>> source.inst.write('*CLS')
(5, <StatusCode.success: 0>)
>>> source.inst.query('SOURce:FREQuency:MODE?')
'CW'
>>> source.inst.query('SOURce:FREQuency:OFFSet?')
'-3.10700000E+008'
>>> source.inst.query('SOURce:FREQuency:OFFSet:STEP:INCRement?')
'+1.00000000E+003'
>>> source.inst.query('SOURce:ROSCillator:SOURce?')
'+1'
>>> source.inst.query('SOURce:SWEep:RSELect?')
'HP8563E'
>>> source.inst.query('SOURce:FREQuency:STEP:AUTO?')
'+1'
>>> source.inst.query('SOURce:POWer:STEP:INCRement?')
'+1.00000000E-001'
>>> source.inst.query('SOURce:FREQuency:STEP:INCRement?')
'+5.00000000E+007'
>>> source.inst.query('SOURce:POWer:ATTenuation?')
'+0'
>>> source.inst.query('SOURce:POWer:CENTer?')
'-5.10000000E+000'
>>> source.inst.query('SOURce:FREQuency:CW?')
'+1.33500000E+010'
>>> source.inst.query('OUTPut:COUPling?')
'AC'
>>> source.inst.query('OUTPut:STATe?')
'+0'
>>>
    '''

    @property
    def OUTPut_COUPling(self):
        self.query('OUTPut:COUPling?')

    @OUTPut_COUPling.setter
    def OUTPut_COUPling(self, COUPling):
        self.write(f'OUTPut:COUPling {COUPling}')

    # coupling = OUTPut_COUPling

    @property
    def frequency(self):
        """."""
        return(self.query("SOURce:FREQuency:CW?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"SOURce:FREQuency:CW {frequency:.0f} Hz")

    @property
    def amplitude(self):
        """."""
        return(self.query("SOURce:POWer:CENTer?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"SOURce:POWer:CENTer {amplitude:.1f} DBM")

    @property
    def output(self):
        """."""
        if self.query("OUTPut:STATe?") == "+1":
            return True
        else:
            return False

    @output.setter
    def output(self, boolean=False):
        self.write(f"OUTPut:STATe {boolean:d}")


class IFR341n():

    def __init__(self, inst):
        self.inst = inst
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    @property
    def frequency(self):
        return float(self.inst.query('SOURce:FREQuency:CW?'))

    @frequency.setter
    def frequency(self, frequency):
        self.inst.write(f'SOURce:FREQuency:CW {frequency:.0f} Hz')

    @property
    def power(self):
        return float(self.inst.query('SOURce:POWer:LEVel:AMPLitude?'))

    @power.setter
    def power(self, power):
        self.inst.write(f'SOURce:POWer:LEVel:AMPLitude {power:.2f} dBm')


REGISTER = {
    'HEWLETT-PACKARD,8657A,': HP8657A,
    'HEWLETT_PACKARD,8664A,': HP8664A,
    'HEWLETT_PACKARD,8665B,': HP8665B,
    'ANRITSU,MG3691B,': AnritsuMG3691B,
    'ANRITSU,MG3692A,': AnritsuMG3692A,
    'ANRITSU,MG3693A,': AnritsuMG3693A,
    'ANRITSU,MG3695B,': AnritsuMG3695B,
    'Agilent Technologies, E4422B,': AgilentE4422B,
    'Hewlett-Packard, ESG-4000B': AgilentE4422B,
    'Wiltron 6669A,': Wiltron6669A,  # TODO
    'Wiltron 6672B,': Wiltron6672B,  # TODO
    'Wiltron 360SS69,': Wiltron360SS69,  # TODO
    'MARCONI INSTRUMENTS,2030': MarconiInstruments2030,
    'MARCONI INSTRUMENTS,2031': MarconiInstruments2031,
    'MARCONI INSTRUMENTS,2032': MarconiInstruments2032,
    'ANRITSU,MG3710A': AnritsuMG3710A,
    'Keysight,N5173B': KeysightN5173B,
    'ROHDE&SCHWARZ,SMH52': RohdeSchwarzSHM52,
    'HEWLETT-PACKARD,85645A,': HP85645A,
    'Agilent Technologies, N5181A,': AgilentN5181A,
    'Agilent Technologies, N5182A,': AgilentN5182A,




    # HP 8673M 2-18GHz
    # Anritsu MG3710A 100e3, 6e9
    # Agilent N5182A 100e3, 6e9
    # Benchview supported E4438C, E4428C, E8267D, E8257D, E8663D, N5171B,N5172B, N5173B, N5181A/B, N5182A/B, N5183A/B
}
