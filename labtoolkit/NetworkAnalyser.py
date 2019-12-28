#!/usr/bin/env python3
"""."""

import time
import logging
# from scipy.interpolate import UnivariateSpline
# import numpy as np

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class NetworkAnalyser(GenericInstrument, IEEE488):
    """Parent class for NetworkAnalysers."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)


class AgilentE8357A(NetworkAnalyser):
    """HP E8357A.

    .. figure::  images/NetworkAnalyser/AgilentE8357A.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    @property
    def points(self):
        """Sweep Points."""
        return int(self.query("SENS1:SWE:POIN?"))

    @points.setter
    def points(self, points=801):
        self.write(f"SENS1:SWE:POIN {int(points)}")

    '''
    CALCulate<cnum>:CORRection[:STATe] <bool>

    '''

    @property
    def bandwidth(self):
        """IF Bandwidth."""
        return float(self.query("SENSe:Bandwidth?"))

    @bandwidth.setter
    def bandwidth(self, bw=1000):
        self.write(f"SENSe:Bandwidth {int(bw)}HZ")

    '''
    @property
    def form(self):
        """Format.

        """
        # LOGM, PHAS, DELA, LINM, SWR, REAL, IMAG, SMITH, POLA, EXPP, ADMIT, SPECT, NOISE, LINY
        return self.query(":CALC1:FORM?")

    @form.setter
    def form(self, form='LOGM'):
        self.write(":CALC1:FORM {}".format(form))

    @property
    def sweepformat(self):
        """Format.

        LOGF, LINF, LIST, POWE
        Log frequency (Network and impedance analyzers only)
        """
        return self.query("SWPT?")

    @sweepformat.setter
    def sweepformat(self, form='LOGF'):
        self.write("SWPT {}".format(form))

    @property
    def paramater(self):
        """Measure paramater.

        AR, RB, R, A, B, S11, S12, S21, S22, IMAG, IPH, IRE, IIM, AMAG, APH, ARE, AIM, RCM, RCPH, RCM, RCPH, RCR, RCIM, CP, CS, LP, LS, D, Q, RP, RS
        """
        return self.query("MEAS?")

    @paramater.setter
    def paramater(self, paramater='S11'):
        self.write("MEAS {}".format(paramater))

    '''
    @property
    def sourcepower(self):
        """Source power dBm."""
        return float(self.query("SOURce:POWer?"))

    @sourcepower.setter
    def sourcepower(self, power=0):
        self.write(f"SOURce:POWer {int(power)}")

    @property
    def start(self):
        """Start frequency."""
        return float(self.query("SENSe:FREQuency:STARt?"))

    @start.setter
    def start(self, frequency):
        self.write(f"SENSe:FREQuency:STARt {frequency}")

    @property
    def stop(self):
        """Stop frequency."""
        return float(self.query("SENSe:FREQuency:STOP?"))

    @stop.setter
    def stop(self, frequency):
        self.write(f"SENSe:FREQuency:STOP {frequency}")

    @property
    def attenuationa(self):
        """Port attenuation A dB."""
        return float(self.query("SENSe:POWer:ATTenuation? ARECeiver"))

    @attenuationa.setter
    def attenuationa(self, attenuation=0):
        self.write(f"SENSe:POWer:ATTenuation? ARECeiver,{int(attenuation)}")

    @property
    def attenuationb(self):
        """Port attenuation B dB."""
        return float(self.query("SENSe:POWer:ATTenuation? BRECeiver"))

    @attenuationb.setter
    def attenuationb(self, attenuation=0):
        self.write(f"SENSe:POWer:ATTenuation? BRECeiver,{int(attenuation)}")

    @property
    def reference(self):
        """returns:.

        EXT is returned when a signal is present at the Reference Oscillator connector
        INT is returned when NO signal is present at the Reference Oscillator connector
        """
        return self.query('SENSe:ROSCillator:SOURce?')

    def trace(self):
        """Get trace."""
        return NotImplemented
        # FORM:DATA ASCII,0
        # FORM:DATA REAL,32
        # FORM:DATA REAL,64
        # FORM:BORDer
        # :CALC1:DATA? FDATA


class HP4395A(NetworkAnalyser):
    """HP 4395A.

    Programming Manual: HP 04395-90031, fifth edition

    .. figure::  images/NetworkAnalyser/HP4395A.jpg
    """

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    @property
    def points(self):
        """Sweep Points, max 801."""
        return int(self.query("POIN?"))

    @points.setter
    def points(self, points=801):
        self.write(f"POIN {int(points)}")

    @property
    def bandwidth(self):
        """IF Bandwidth.

        2, 10, 30, 100, 300, 1000 (=1k), 3000 (=3k), 10000 (=10k), 30000 (=30k)
        """
        return float(self.query("BW?"))

    @bandwidth.setter
    def bandwidth(self, points=1000):
        self.write(f"BW {int(points)}HZ")

    @property
    def form(self):
        """Format.

        LOGM, PHAS, DELA, LINM, SWR, REAL, IMAG, SMITH, POLA, EXPP, ADMIT, SPECT, NOISE, LINY
        """
        return self.query("FMT?")

    @form.setter
    def form(self, form='LOGM'):
        self.write(f"FMT {form}")

    @property
    def sweepformat(self):
        """Format.

        LOGF, LINF, LIST, POWE
        Log frequency (Network and impedance analyzers only)
        """
        return self.query("SWPT?")

    @sweepformat.setter
    def sweepformat(self, form='LOGF'):
        self.write(f"SWPT {form}")

    @property
    def paramater(self):
        """Measure paramater.

        AR, RB, R, A, B, S11, S12, S21, S22, IMAG, IPH, IRE, IIM, AMAG, APH, ARE, AIM, RCM, RCPH, RCM, RCPH, RCR, RCIM, CP, CS, LP, LS, D, Q, RP, RS
        """
        return self.query("MEAS?")

    @paramater.setter
    def paramater(self, paramater='S11'):
        self.write(f"MEAS {paramater}")

    @property
    def attenuationr(self):
        """Port attenuation R dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.query("ATTR?"))

    @attenuationr.setter
    def attenuationr(self, attenuation=20):
        self.write(f"ATTR {int(attenuation)}DB")

    @property
    def attenuationa(self):
        """Port attenuation A dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.query("ATTA?"))

    @attenuationa.setter
    def attenuationa(self, attenuation=20):
        self.write(f"ATTA {int(attenuation)}DB")

    @property
    def attenuationb(self):
        """Port attenuation B dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.query("ATTB?"))

    @attenuationb.setter
    def attenuationb(self, attenuation=20):
        self.write(f"ATTB {int(attenuation)}DB")

    @property
    def sourcepower(self):
        """Source power dBm."""
        return float(self.query("POWE?"))

    @sourcepower.setter
    def sourcepower(self, power=0):
        self.write(f"POWE {int(power)}")

    @property
    def start(self):
        """Start frequency."""
        return float(self.query("STAR?"))

    @start.setter
    def start(self, frequency):
        self.write(f"STAR {frequency}")

    @property
    def stop(self):
        """Stop frequency."""
        return float(self.query("STOP?"))

    @stop.setter
    def stop(self, frequency):
        self.write(f"STOP {frequency}")

    def trace(self):
        """Get formatted trace."""
        return NotImplemented
        '''
         inst.timeout = 30000
        # inst.write("FORM4")
        print(inst.query("OUTPDATA?"))
        # print(inst.query("OUTPSWPRM?"))
        '''
        '''

53 54 41 52 3F                                  STAR?
53 54 4F 50 3F                                  STOP?
4E 41 3F                                        NA?

31 0A                                           1.

4D 45 41 53 3F                                  MEAS?

46 4F 52 4D 34 3B                               FORM4;

4F 55 54 50 44 54 52 43 3F                      OUTPDTRC?
        '''


class Wiltron360(NetworkAnalyser):
    """Wiltron 360.

    .. figure::  images/NetworkAnalyser/Wiltron360.jpg
    """

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    def trace(self):
        """Get trace."""
        return NotImplemented
    '''
    with ResourceManager('') as rm:
        # 'Sim/default.yaml@sim' '@py', 'ni'

        addrs = visaaddresslist([6], suffix="::INSTR")
        # print(addrs)
        wiltron = Instrument(rm, addrs[0], read_termination='')
        # print(wiltron.inst.query_ascii_values("OFV"))  # OFV, OCD
        # wiltron.inst.write('FMA')
        # time.sleep(1)
        # data = wiltron.inst.query_binary_values('FMC MSB OFV', delay=0.2)
        wiltron.inst.write('FMC MSB OCD')
        data = wiltron.inst.read_raw()
        print(data)
    '''


class KeysightFieldFox(NetworkAnalyser):
    """Keysight FieldFox.

    .. figure::  images/NetworkAnalyser/KeysightFieldFoxN9928A.jpg
    """

    def __init__(self, instrument, logger=None):
        """."""
        super().__init__(instrument)
        # self.log = logging.getLogger(__name__)
        self.freqs = [30e3, 26.5e9]
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')
        # self.log.info('Creating an instance of\t' + str(__class__))

        self.write("*CLS")  # clear error status

    def __repr__(self):
        """."""
        return(f"{__class__.__name__}, {self.instrument}")

    @property
    def points(self):
        """Sweep Points, max 10,001."""
        return(self.query("SENS:SWE:POIN?"))

    @points.setter
    def points(self, points):
        self.write(f"SENS:SWE:POIN {points:.0f}")

    @property
    def start(self):
        """Start frequency."""
        return(self.query("SENS:FREQ:STAR?"))

    @start.setter
    def start(self, start):
        self.write(f"SENS:FREQ:STAR {start:.0f}Hz")

    @property
    def stop(self):
        """Stop frequency."""
        return(self.query("SENS:FREQ:STOP?"))

    @stop.setter
    def stop(self, stop):
        self.write(f"SENS:FREQ:STOP {stop:.0f}Hz")

    @property
    def bandwidth(self):
        """IF bandwidth."""
        return(self.query(":BWID?"))

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        self.write(f":BWID {bandwidth:.0f}")

    @property
    def display(self):
        """."""
        return(self.query("DISP:ENAB?"))

    @display.setter
    def display(self, display):
        self.write(f"DISP:ENAB {display:d}")

    @property
    def trigger(self):
        """."""
        return(self.query("INIT:CONT?"))

    @trigger.setter
    def trigger(self, trigger):
        self.write(f"INIT:CONT {trigger:d}")

    @property
    def format(self):
        """."""
        return(self.query("CALC:SEL:FORM?"))

    @format.setter
    def format(self, form):
        self.write(f"CALC:SEL:FORM {form}")

    @property
    def sparameter(self):
        """."""
        return(self.query("CALC:PAR1:DEF?"))

    @sparameter.setter
    def sparameter(self, sparameter="S11"):  # S21, S12, S22
        self.write(f"CALC:PAR1:DEF {sparameter}")

    def sweep(self):
        """."""
        self.write("INIT")
        self.write("*WAI")

    def readRI(self):
        """."""
        self.write("CALC:DATA:SDAT?")
        answer = self.engineering_project.read_until(b'\n').decode('ascii')
        parsed = answer.strip().split(",")
        real = [float(parsed[i]) for i in range(0, len(parsed), 2)]
        imag = [float(parsed[i]) for i in range(1, len(parsed), 2)]
        return (real, imag)

    def readFormatted(self):
        """."""
        self.write("CALC:DATA:FDAT?")
        answer = self.engineering_project.read_until(b'\n').decode('ascii')
        parsed = answer.strip().split(",")
        return ([float(x) for x in parsed], [0.0]*len(parsed))
    # topfreq = freq + span/2
    # botfreq = freq - span/2


REGISTER = {
    "Keysight, Fieldfox": KeysightFieldFox,
    'HEWLETT-PACKARD,4395A,': HP4395A,
    'Agilent Technologies,E8357A': AgilentE8357A,
    'Wiltron360': Wiltron360,
    # Benchview suppored:
    # ENA:  E5080A, E5061B, E5063A, E5071C, E5072A
    # PNA:  N5221A, N5222A, N5224A, N5245A, N5227A
    # PNA-L:  N5230C, N5231A, N5232A, N5234A, N5235A, N5239A
    # PNA-X:  N5241A, N5242A, N5244A, N5245A, N5247A, N5249A
    # Fieldfox: N9912A, N9913A, N9914A, N9915A, N9916A, N9917A, N9918A, N9923A, N9925A, N9926A, N9927A, N9928A, N9935A, N9936A, N9937A, N9938A, N9950A, N9951A, N9952A, N9960A, N9961A, N9962A
}
