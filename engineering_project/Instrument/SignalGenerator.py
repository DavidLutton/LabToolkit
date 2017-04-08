#!/usr/bin/env python3
import time
import logging

from Instrument.GenericInstrument import GenericInstrument as GenericInstrument


class SignalGenerator(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)
        self.amplimit = 0

    def safe(self):
        self.amplitude = min(self.amps)
        self.frequency = min(self.freqs)
        self.output = False

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

#    def __preset__(self):
#        self.safe()
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
    def amplitude(self, amplitude):
        self.write("SOURce:POWer:LEVel:AMPLitude {0:.2f} DBM".format(amplitude))

    '''
    def amp(self, amplitude):
        if self.amplitude != amplitude:
            if amplitude <= self.amplimit:  # prevent resubmitting request to set the same frequency

                self.amplitude = amplitude
            else:
                self.log.warn("on " + self.IDN + " exceeded amplimit")
    '''

    @property
    def output(self):
        self.query("OUTPut:STATe?")

    @output.setter
    def output(self, boolean):
        self.write("OUTPut:STATe {}".format(boolean))


'''class HP8664A(SignalGenerator):

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
        self.frequency = self.query("FREQ:CW?")
        self.amplitude = self.query("AMPL:OUT:LEV?")
        # self.siggen.write("*CLS")  # clear error status

    def __preset__(self):
        self.safe()

    def freq(self, freq):
        self.freqsetter("FREQ:CW {0:.0f}Hz".format(freq))

    def amp(self, amplitude):
        if self.amplitude != amplitude:
            if amplitude <= self.amplimit:  # prevent resubmitting request to set the same frequency
                self.write("AMPL:OUT:LEV {0:.1f}DBM".format(amplitude))
                self.amplitude = amplitude

                # time.sleep(.3)  # after leveling wait time for settling
            else:
                self.log.warn("on " + self.IDN + " exceeded amplimit")

    def enable(self):
        pass  # self.write("OUTP:STAT ON")

    def disable(self):
        pass  # self.write("OUTP:STAT OFF")


class HP8665B(SignalGenerator):

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
        self.frequency = self.query("FREQ:CW?")
        self.amplitude = self.query("AMPL:OUT:LEV?")
        # self.siggen.write("*CLS")  # clear error status

    def __preset__(self):
        self.safe()

    def freq(self, freq):
        self.freqsetter("FREQ:CW {0:.0f}Hz".format(freq))

    def amp(self, amplitude):
        if self.amplitude != amplitude:
            if amplitude <= self.amplimit:  # prevent resubmitting request to set the same frequency
                self.write("AMPL:OUT:LEV {0:.1f}DBM".format(amplitude))
                self.amplitude = amplitude

                # time.sleep(.3)  # after leveling wait time for settling
            else:
                self.log.warn("on " + self.IDN + " exceeded amplimit")

    def enable(self):
        pass  # self.write("OUTP:STAT ON")

    def disable(self):
        pass  # self.write("OUTP:STAT OFF")


class HP8657A(SignalGenerator):
    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('HEWLETT-PACKARD,8657A,')
        self.amps = [-111, 17]
        self.freqs = [100e3, 1040e6]
        self.frequency = self.query("FR?")
        self.amplitude = self.query("AP?")
        # self.siggen.write("*CLS")  # clear error status
        self.__preset__()

    def __preset__(self):
        self.safe()

    def freq(self, freq):
        self.freqsetter("FR {0:.0f}Hz".format(freq))

    def amp(self, amplitude):
        if self.amplitude != amplitude:
            if amplitude <= self.amplimit:  # prevent resubmitting request to set the same frequency
                self.write("AP {0:.1f}DM".format(amplitude))
                self.amplitude = amplitude

                # time.sleep(.3)  # after leveling wait time for settling
            else:
                self.log.warn("on " + self.IDN + " exceeded amplimit")

    def enable(self):
        pass  # self.write("OUTP:STAT ON")

    def disable(self):
        pass  # self.write("OUTP:STAT OFF")


class AgilentE4422B(SignalGenerator):
    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('Agilent Technologies, E4422B')

        self.frequency = self.query("FREQ?")
        self.amplitude = self.query("POW:AMPL?")
        self.amps = [-100, 16]
        self.freqs = [100e3, 4e9]
        self.write("*CLS")  # clear error status
        self.safe()

    def freq(self, freq):
        if self.frequency != freq:  # prevent resubmitting request to set the same frequency
            self.write("FREQ {0:.0f} Hz".format(freq))
            self.frequency = freq
            time.sleep(.3)  # after retuneing wait time for settling

    def amp(self, amplitude):
        if self.amplitude != amplitude:
            if amplitude <= self.amplimit:  # prevent resubmitting request to set the same frequency
                self.write("POW:AMPL {0:.1f} dBm".format(amplitude))
                self.amplitude = amplitude

                # time.sleep(.3)  # after leveling wait time for settling
            else:
                self.log.warn("on " + self.IDN + " exceeded amplimit")

    def enable(self):
        self.write("OUTP:STAT ON")

    def disable(self):
        self.write("OUTP:STAT OFF")


class AnritsuMG3691B(SignalGenerator):  # ANRITSU,MG3691B,
    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('ANRITSU,MG3691B,')

        self.frequency = self.query("OF0")
        self.amplitude = self.query("OLO")
        self.amps = [-110, 30]
        self.freqs = [10e6, 10e9]
        self.write("*CLS")  # clear error status
        self.__preset__()

    def __preset__(self):
        self.safe()
        self.write('RL1')  # Release to Local

    def freq(self, freq):
        if self.frequency != freq:  # prevent resubmitting request to set the same frequency
            self.write("F0{0:.0f} HZ".format(freq))
            self.frequency = freq
            time.sleep(.3)  # after retuneing wait time for settling

    def amp(self, amplitude):
        if self.amplitude != amplitude:
            if amplitude <= self.amplimit:  # prevent resubmitting request to set the same frequency
                self.write("L0{0:.1f}DM".format(amplitude))
                self.amplitude = amplitude

                # time.sleep(.3)  # after leveling wait time for settling
            else:
                self.log.warn("on " + self.IDN + " exceeded amplimit")

    def enable(self):
        self.write("RF1")

    def disable(self):
        self.write("RF0")


class AnritsuMG3693A(SignalGenerator):  # ANRITSU,MG3693A,
    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('ANRITSU,MG3693A,')

        self.frequency = self.query("OF0")
        self.amplitude = self.query("OLO")
        self.amps = [-110, 30]  # ???
        self.freqs = [2e9, 30e9]
        self.write("*CLS")  # clear error status
        self.__preset__()

    def __preset__(self):
        self.safe()
        self.write('RL1')  # Release to Local

    def freq(self, freq):
        if self.frequency != freq:  # prevent resubmitting request to set the same frequency
            self.write("F0{0:.0f} HZ".format(freq))
            self.frequency = freq
            time.sleep(.3)  # after retuneing wait time for settling

    def amp(self, amplitude):
        if self.amplitude != amplitude:
            if amplitude <= self.amplimit:  # prevent resubmitting request to set the same frequency
                self.write("L0{0:.1f}DM".format(amplitude))
                self.amplitude = amplitude

                # time.sleep(.3)  # after leveling wait time for settling
            else:
                self.log.warn("on " + self.IDN + " exceeded amplimit")

    def enable(self):
        self.write("RF1")

    def disable(self):
        self.write("RF0")


class AnritsuMG3692A(SignalGenerator):  # ANRITSU,MG3692A,
    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        assert self.IDN.startswith('ANRITSU,MG3692A,')

        self.frequency = self.query("OF0")
        self.amplitude = self.query("OLO")
        self.amps = [-110, 30]
        self.freqs = [10e6, 20e9]
        self.write("*CLS")  # clear error status
        self.__preset__()

    def __preset__(self):
        self.safe()
        self.write('RL1')  # Release to Local

    def freq(self, freq):
        if self.frequency != freq:  # prevent resubmitting request to set the same frequency
            self.write("F0{0:.0f} HZ".format(freq))
            self.frequency = freq
            time.sleep(.3)  # after retuneing wait time for settling

    def amp(self, amplitude):
        if self.amplitude != amplitude:
            if amplitude <= self.amplimit:  # prevent resubmitting request to set the same frequency
                self.write("L0{0:.1f}DM".format(amplitude))
                self.amplitude = amplitude

                # time.sleep(.3)  # after leveling wait time for settling
            else:
                self.log.warn("on " + self.IDN + " exceeded amplimit")

    def enable(self):
        self.write("RF1")

    def disable(self):
        self.write("RF0")
'''
