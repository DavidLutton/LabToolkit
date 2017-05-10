#!/usr/bin/env python3
import time
import logging
import pint

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class SignalGenerator(GenericInstrument):
    def __init__(self, instrument):
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

    Applied by decorator @amplitudelimiter"""
    def __init__(self, f, *args, **kwargs):
        """
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        # print(f)
        # print(*args)
        # print(**kwargs)
        # print("Inside __init__()")
        self.f = f

    def __call__(self, f, *args, **kwargs):
        """
        The __call__ method is not called until the
        decorated function is called.
        """
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


class SCPI(SignalGenerator):
    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        self.amps = [-140, 17]
        self.freqs = [100e3, 3e9]
        # self.siggen.write("*CLS")  # clear error status
        # self.frequency = min(self.freqs)

    @property
    def frequency(self):
        return(self.query("SOURce:FREQuency:CW?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("SOURce:FREQuency:CW {0:.0f} Hz".format(frequency))

    @property
    def amplitude(self):
        return(self.query("SOURce:POWer:LEVel:AMPLitude?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("SOURce:POWer:LEVel:AMPLitude {0:.2f} DBM".format(amplitude))

    @property
    def output(self):
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))


class HP8657A(SignalGenerator):
    """HP 8657A 100e3, 1040e6."""
    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
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
        return(self.query("FR?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("FR {0:.0f}Hz".format(frequency))

    @property
    def amplitude(self):
        return(self.query("AP?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("AP {0:.1f}DM".format(amplitude))

    @property
    def output(self):
        pass

    @output.setter
    def output(self, boolean=False):
        if boolean is False:
            self.write("R2")
        else:
            if boolean is True:
                self.write("R3")


class HP8664A(SignalGenerator):
    """HP 8664A 100e3, 3e9.

    .. figure::  images/SignalGenerator/HP8664A.jpg"""

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('HEWLETT_PACKARD,8664A,')
        self.amps = [-140, 17]
        self.freqs = [100e3, 3e9]

    @property
    def frequency(self):
        return(self.query("FREQ:CW?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("FREQ:CW {0:.0f}Hz".format(frequency))

    @property
    def amplitude(self):
        return(self.query("AMPL:OUT:LEV?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("AMPL:OUT:LEV {0:.1f}DBM".format(amplitude))
    '''
    @property
    def output(self):
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))
    '''


class HP8665B(SignalGenerator):
    """HP 8665B 100e3, 6e9.

    .. figure::  images/SignalGenerator/HP8665B.jpg
    """

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('HEWLETT_PACKARD,8665B,')
        self.amps = [-140, 17]
        self.freqs = [100e3, 6e9]

    @property
    def frequency(self):
        return(self.query("FREQ:CW?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("FREQ:CW {0:.0f}Hz".format(frequency))

    @property
    def amplitude(self):
        return(self.query("AMPL:OUT:LEV?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("AMPL:OUT:LEV {0:.1f}DBM".format(amplitude))
    '''
    @property
    def output(self):
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))
    '''


class AgilentN5182A(SignalGenerator):
    """Agilent N5182A 100e3, 6e9

    .. figure::  images/SignalGenerator/AgilentN5182A.jpg
    """


class AgilentE4422B(SignalGenerator):
    """Agilent E4422B 250e3, 4e9.

    .. figure::  images/SignalGenerator/AgilentE4422B.jpg
    """

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('Agilent Technologies, E4422B')

        self.amps = [-100, 16]
        self.freqs = [100e3, 4e9]
        # self.write("*CLS")  # clear error status

    @property
    def frequency(self):
        return(self.query("FREQ?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("FREQ {0:.0f} Hz".format(frequency))

    @property
    def amplitude(self):
        return(self.query("POWer?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("POWer {0:.2f} dBm".format(amplitude))

    @property
    def output(self):
        if self.query("OUTPut:STATe?") == "1":
            return(True)
        else:
            return(False)

    @output.setter
    def output(self, boolean=False):
        self.write("OUTPut:STATe {:d}".format(boolean))  # OUTP:STAT ON // OFF


class AnritsuMG369nx(SignalGenerator):  # ANRITSU,MG369nx
    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
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
        return(self.query("OF0"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("F0{0:.0f} HZ".format(frequency))

    @property
    def amplitude(self):
        return(self.query("OL0"))  # OLO

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write("L0{0:.2f}DM".format(amplitude))

    @property
    def output(self):
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
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
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
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
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
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('ANRITSU,MG3693A,')

        self.amps = [-110, 30]
        self.freqs = [2e9, 30e9]


class Willtronnnnn(SignalGenerator):
    """Willtron 10e6, 40e9."""

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
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
        return(self.query("OF0"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("F0{0:.2f}GH".format(frequency))

    @property
    def amplitude(self):
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


class WilltronHeadless(SignalGenerator):
    """Willtron Headless 10e6, 40e9."""

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
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
        return(self.query("OF0"))

    @frequency.setter
    def frequency(self, frequency):
        self.write("F0{0:.2f}GH".format(frequency))

    @property
    def amplitude(self):
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


'''inst = rm.open_resource('GPIB0::6::INSTR')
print( inst.query('*IDN?').strip() )
print( inst.write('CFRQ:VALUE 1234.5678912MHZ') )


# MARCONI INSTRUMENTS,2032,119500001,5.002
# E266'''

register = {
    "HEWLETT-PACKARD,8657A,": HP8657A,
    "HEWLETT_PACKARD,8664A,": HP8664A,
    "HEWLETT_PACKARD,8665B,": HP8665B,
    "ANRITSU,MG3691B,": AnritsuMG3691B,
    "ANRITSU,MG3692A,": AnritsuMG3692A,
    "ANRITSU,MG3693A,": AnritsuMG3693A,
    "Agilent Technologies, E4422B,": AgilentE4422B,
    "Hewlett-Packard, ESG-4000B": AgilentE4422B,
    "Willtron ZZZZ,": Willtronnnnn,
    #
    # HP 8673M 2-18GHz
    # Anritsu MG3710A 100e3, 6e9
    # Agilent N5182A 100e3, 6e9
    # Marconi 2031 10e3-2.7e9
    # Marconi 20nn 10e3-5.4e9
}
