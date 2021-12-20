from ..IEEE488 import IEEE488
from ..SCPI import SCPI
import numpy as np
import pandas as pd


class AgilentE8357A(IEEE488, SCPI):
    """HP E8357A.

    .. figure::  images/NetworkAnalyser/AgilentE8357A.jpg
    """

    def trace(self, trace='S21'):
        x = self.readX()
        y = self.readS(trace, self.catalog())
        db = 20 * np.log10(np.abs(y))
        df = pd.DataFrame(
            np.column_stack(([x, db, y.real, y.imag])), 
            columns=['Frequency (Hz)', 'dB', 'Real', 'Imag']
        )
        return df.set_index('Frequency (Hz)')

    def catalog(self):
        string = self.query('CALC1:PAR:CAT?')  # string='"CH1_S11_1,S11,CH1_S21_2,S21,CH1_S12_3,S12,CH1_S22_4,S22,ADIVB,R1/A"'
        index = string.strip('"').split(',')
        # l = ['CH1_S11_1', 'S11', 'CH1_S21_2', 'S21', 'CH1_S12_3', 'S12', 'CH1_S22_4', 'S22', 'ADIVB', 'R1/A']
        catalog = {}
        for i, x in enumerate(index[::2]):  # every other
            # print(x)
            # print(l[(i*2)+1])
            catalog[index[(i * 2) + 1]] = x
        # catlog = {'S11': 'CH1_S11_1', 'S21': 'CH1_S21_2', 'S12': 'CH1_S12_3', 'S22': 'CH1_S22_4', 'R1/A': 'ADIVB'}
        return catalog

    def readX(self):
        sweeptype = self.query('SENS1:SWE:TYPE?')
        '''
        SENS1:SWE:TYPE? "SEGM"
        SENS1:SEGM:COUN? +1
        SENS1:SEGM1:STATE? 1
        SENS1:SEGM1:FREQ:STAR? +3.00000000000E+005
        SENS1:SEGM1:FREQ:STOP? +5.00000000000E+006
        SENS1:SEGM1:SWE:POIN? +500
        '''
        # print(sweeptype)
        start, stop, step = self.query_float('SENS1:FREQ:STAR?'), self.query_float('SENS1:FREQ:STOP?'), self.query_int('SENS1:SWE:POIN?')
        if sweeptype == 'LIN':
            return np.linspace(start, stop, step)
        elif sweeptype == 'LOG':
            return np.geomspace(start, stop, step)
        elif sweeptype == 'POW':
            start, stop = self.query_float('SOUR1:POW:STAR?'), self.query_float('SOUR1:POW:STOP?')
            return np.linspace(start, stop, step)
        else:
            return None

    def readS(self, nn, cat):
        timeout = self.inst.timeout
        self.inst.timeout = 3000

        # print('CALC1:PAR:SEL \'{}\''.format(cat[nn]))
        self.write('CALC1:PAR:SEL \'{}\''.format(cat[nn]))

        self.write('FORM:BORD SWAP')
        self.write('FORM:DATA REAL,32')
        arr = self.query_binary_values(':CALC1:DATA? SDATA', container=np.float64).view(np.complex128)

        # self.inst.write('FORM:BORD NORM')
        # self.inst.write('FORM:DATA ASCII,0')
        # arr = self.inst.query_ascii_values(':CALC1:DATA? SDATA', container=np.float64).view(np.complex128)

        self.inst.timeout = timeout
        return arr
        # read as a RI series of floats and .view as complex

        # Array of float consisting of interleaved real imag >>> array when .view as complex
        # array([1., 2., 3., 4., 5., 6.]).view(np.complex128) >>> array([1.+2.j, 3.+4.j, 5.+6.j])

        # Note cannot go direct to complex as numpy would produce
        # np.array([1., 2., 3., 4., 5., 6.], dtype=np.complex128) >>> array([1.+0j, 2.+0.j, 3.+0.j, 4.+0.j, 5.+0.j, 6.+0.j])

        # You can access the real and imag components
        # array([1.+2.j, 3.+4.j, 5.+6.j]).real >>> array([1., 3., 5.])
        # array([1.+2.j, 3.+4.j, 5.+6.j]).imag >>> array([2., 4., 6.])

    @property
    def points(self):
        """Sweep Points."""
        return self.query_int("SENS1:SWE:POIN?")

    @points.setter
    def points(self, points=801):
        self.write(f"SENS1:SWE:POIN {int(points)}")

    '''
    CALCulate<cnum>:CORRection[:STATe] <bool>

    '''

    @property
    def bandwidth(self):
        """IF Bandwidth."""
        return self.query_float("SENSe:Bandwidth?")

    @bandwidth.setter
    def bandwidth(self, bw=1000):
        self.write(f"SENSe:Bandwidth {int(bw)}HZ")

    @property
    def sourcepower(self):
        """Source power dBm."""
        return self.query_float("SOURce:POWer?")

    @sourcepower.setter
    def sourcepower(self, power=0):
        self.write(f"SOURce:POWer {int(power)}")

    @property
    def start(self):
        """Start frequency."""
        return self.query_float("SENSe:FREQuency:STARt?")

    @start.setter
    def start(self, frequency):
        self.write(f"SENSe:FREQuency:STARt {frequency}")

    @property
    def stop(self):
        """Stop frequency."""
        return self.query_float("SENSe:FREQuency:STOP?")

    @stop.setter
    def stop(self, frequency):
        self.write(f"SENSe:FREQuency:STOP {frequency}")

    @property
    def reference(self):
        """returns:.

        EXT is returned when a signal is present at the Reference Oscillator connector
        INT is returned when NO signal is present at the Reference Oscillator connector
        """
        return self.query('SENSe:ROSCillator:SOURce?')


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


    def trace(self):
        """Get trace."""
        return NotImplemented
        # FORM:DATA ASCII,0
        # FORM:DATA REAL,32
        # FORM:DATA REAL,64
        # FORM:BORDer
        # :CALC1:DATA? FDATA

    '''
