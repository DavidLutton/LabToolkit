#!/usr/bin/env python3
import time
import logging
import pint

try:
    from Instrument.GenericInstrument import GenericInstrument
    from Instrument.IEEE488 import IEEE488
    from Instrument.SCPI import SCPI

except ImportError:
    from GenericInstrument import GenericInstrument
    from IEEE488 import IEEE488
    from SCPI import SCPI


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
        self.frequency = min(self.freqs)

    def state(self):
        """Report basic paramaters."""
        print("Amplitude: {}".format(self.amplitude))
        print("Frequency: {}".format(self.frequency))
        print("Output: {}".format(self.output))

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
            f.log.warn("Amplimit ({}) reached with setpoint ({}) on {}".format(f.amplimit, setpoint, f.instrument))
        else:
            self.f(f, *args)
        # print("After self.f(*args)")


class SCPISignalGenerator(SignalGenerator, IEEE488, SCPI):
    """."""

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
        self.write("SOURce:FREQuency:CW {0:.0f} Hz".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("SOURce:POWer:LEVel:AMPLitude?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("SOURce:POWer:LEVel:AMPLitude {0:.2f} DBM".format(amplitude))

    @property
    def output(self):
        """."""
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))


class HP8657A(SignalGenerator, IEEE488):
    """HP 8657A 100e3, 1040e6.

    .. figure::  images/SignalGenerator/HP8657A.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
        self.write("FR {0:.0f}Hz".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("AP?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("AP {0:.1f}DM".format(amplitude))

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

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    @property
    def frequency(self):
        """."""
        return(self.query("FREQ:CW?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("FREQ:CW {0:.0f}Hz".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("AMPL:OUT:LEV?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("AMPL:OUT:LEV {0:.1f}DBM".format(amplitude))

    @property
    def output(self):
        if self.query("AMPL:OUT:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("AMPL:OUT:STATe {:d}".format(boolean))


class HP8664A(HP866nA):
    """HP 8664A 100e3, 3e9.

    .. figure::  images/SignalGenerator/HP8664A.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('HEWLETT_PACKARD,8664A,')
        self.amps = [-140, 17]
        self.freqs = [100e3, 3e9]


class HP8665B(HP866nA):
    """HP 8665B 100e3, 6e9.

    .. figure::  images/SignalGenerator/HP8665B.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('HEWLETT_PACKARD,8665B,')
        self.amps = [-140, 17]
        self.freqs = [100e3, 6e9]


class AgilentN5182A(SignalGenerator, IEEE488):
    """Agilent N5182A 100e3, 6e9.

    .. figure::  images/SignalGenerator/AgilentN5182A.jpg
    """


class AgilentN5181A(SignalGenerator, IEEE488):
    """Agilent N5181A 100e3, 3e9.

    .. figure::  images/SignalGenerator/AgilentN5181A.jpg
    """


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
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
        self.write("FREQ {0:.0f} Hz".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("POWer?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("POWer {0:.2f} dBm".format(amplitude))

    @property
    def output(self):
        """."""
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))  # OUTP:STAT ON // OFF


class AnritsuMG369nx(SignalGenerator, IEEE488):
    """ANRITSU,MG369nx."""

    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))
        # self.options = self.query("*OPT?").strip().split(',')

        # self.amps = [-110, 30]
        self.freqs = [2e9, 10e9]
        # self.write("*CLS")  # clear error status
        self.write('RL1')  # Release to Local

    @property
    def frequency(self):
        """."""
        return(self.query("OF0"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("F0{0:.0f} HZ".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))  # OLO

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("L0{0:.2f}DM".format(amplitude))

    @property
    def output(self):
        """."""
        pass
        ''' ORF if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)
        '''

    @output.setter
    def output(self, boolean=False):
        self.write("RF{:d}".format(boolean))


class AnritsuMG3691B(AnritsuMG369nx):  # ANRITSU,MG3691B,
    """Antitsu MG3691B 2e9, 10e9.

    .. figure::  images/SignalGenerator/AnritsuMG3691B.jpg
    """

    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('ANRITSU,MG3691B,')

        self.amps = [-110, 30]
        self.freqs = [10e6, 10e9]


class AnritsuMG3692A(AnritsuMG369nx):  # ANRITSU,MG3692A,
    """Antitsu MG3692A 2e9, 20e9.

    .. figure::  images/SignalGenerator/AnritsuMG3692A.jpg
    """

    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('ANRITSU,MG3692A,')

        self.amps = [-110, 30]
        self.freqs = [10e6, 20e9]


class AnritsuMG3693A(AnritsuMG369nx):  # ANRITSU,MG3693A,
    """Antitsu MG3693A 2e9, 30e9.

    .. figure::  images/SignalGenerator/AnritsuMG3693A.jpg
    """

    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('ANRITSU,MG3693A,')

        self.amps = [-110, 30]
        self.freqs = [2e9, 30e9]


class Wiltron6669A(SignalGenerator, IEEE488):
    """Wiltron 6669A 10e6, 40e9.

    .. figure::  images/SignalGenerator/Wiltron6669A.jpg
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
        self.write("F0{0:.2f}GH".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("L0{0:.2f}DM".format(amplitude))

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
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
        self.write("F0{0:.2f}GH".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("L0{0:.2f}DM".format(amplitude))

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
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
        self.write("F0{0:.2f}GH".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("L0{0:.2f}DM".format(amplitude))

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
    """

    @property
    def frequency(self):
        """."""
        return(self.query("CFRQ?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("CFRQ:VALUE {0:.1f}Hz".format(frequency))

    @property
    def amplitude(self):
        """."""
        return(self.query("RFLV?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("RFLV:VALUE {0:.2f}DBM".format(amplitude))

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

    .. figure::  images/SignalGenerator/MarconiInstruments2030.jpg
    10 kHz to 1.35 GHz (2030)
    """

    def __repr__(self):
        """."""
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

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


REGISTER = {
    'HEWLETT-PACKARD,8657A,': HP8657A,
    'HEWLETT_PACKARD,8664A,': HP8664A,
    'HEWLETT_PACKARD,8665B,': HP8665B,
    'ANRITSU,MG3691B,': AnritsuMG3691B,
    'ANRITSU,MG3692A,': AnritsuMG3692A,
    'ANRITSU,MG3693A,': AnritsuMG3693A,
    'Agilent Technologies, E4422B,': AgilentE4422B,
    'Hewlett-Packard, ESG-4000B': AgilentE4422B,
    'Wiltron 6669A,': Wiltron6669A,  # TODO
    'Wiltron 6672B,': Wiltron6672B,  # TODO
    'Wiltron 360SS69,': Wiltron360SS69,  # TODO
    'MARCONI INSTRUMENTS,2030': MarconiInstruments2030,
    'MARCONI INSTRUMENTS,2031': MarconiInstruments2031,
    'MARCONI INSTRUMENTS,2032': MarconiInstruments2032,

    # HP 8673M 2-18GHz
    # Anritsu MG3710A 100e3, 6e9
    # Agilent N5182A 100e3, 6e9
}
