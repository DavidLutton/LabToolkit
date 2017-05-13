#!/usr/bin/env python3
import time
import logging
import pint

try:
    from Instrument.GenericInstrument import GenericInstrument as GenericInstrument
except ImportError:
    from GenericInstrument import GenericInstrument as GenericInstrument


class WaveformGenerator(GenericInstrument):
    def __init__(self, instrument):
        super().__init__(instrument)

    def safe(self):
        self.amplitude = min(self.amps)
        # self.frequency = min(self.freqs)
        # self.output = False

    def state(self):
        print("Amplitude: {}".format(self.amplitude))
        print("Frequency: {}".format(self.frequency))
        print("Shape: {}".format(self.shape))
        print("Load: {}".format(self.load))
        # print("Output: {}".format(self.output))

    def start(self, lvl=-50):
        self.amplitude = lvl


class amplitudelimiter(object):

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


class HP33120A(WaveformGenerator):
    """HP 33120A, 0 to 15MHz.

    .. figure::  images/WaveformGenerator/HP33120A.jpg"""
    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        super().__init__(instrument)
        self.amplimit = 5
        self.log.info('Creating {} for {}'.format(str(__class__.__name__), self.instrument))

        # assert self.IDN.startswith('HEWLETT-PACKARD,???,')
        self.amps = [0.01, 5]
        self.freqs = [0, 15e6]

        # self.siggen.write("*CLS")  # clear error status

        # self.safe()
        # self.state()

    @property
    def frequency(self):
        return(float(self.query("SOURce:FREQuency?")))

    @frequency.setter
    def frequency(self, frequency):
        self.write("SOURce:FREQuency {0:.4f}".format(frequency))

    @property
    def shape(self):
        return(self.query("SOURce:FUNCtion:SHAPe?"))

    @shape.setter
    def shape(self, shape="SIN"):
        # SIN|SQU|TRI|RAMP|NOIS|DC|USER
        self.write("SOURce:FUNCtion:SHAPe {}".format(shape))

    @property
    def load(self):
        return(self.query("OUTPut:LOAD?"))

    @load.setter
    def load(self, load="INF"):
        # 50 | INF | MAX | MIB
        self.write("OUTPut:LOAD {}".format(load))

    @property
    def amplitude(self):
        self.query("SOURce:VOLTage:UNIT?")
        return(float(self.query("SOURce:VOLTage?")))
        # return(self.query("SOURce:VOLTage:UNIT?"))

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude, unit="VPP"):
        # VPP|VRMS|DBM|DEF
        self.write("SOURce:VOLTage {0:.6f}{1}".format(amplitude, unit))


class HP8116A(WaveformGenerator):
    """HP 8116A, 0 to 50MHz.

    .. figure::  images/WaveformGenerator/HP8116A.jpg
    """


class Keysight33500B(WaveformGenerator):
    """Keysight 33500B, 0 to 20MHz.

    .. figure::  images/WaveformGenerator/Keysight33500B.jpg
    """


register = {
    "HEWLETT-PACKARD,33120A,": HP33120A,
}
