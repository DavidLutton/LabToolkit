import numpy as np
import pandas as pd

from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class AnritsuShockline(IEEE488, SCPI):
    """https://dl.cdn-anritsu.com/en-us/test-measurement/files/Manuals/Programming-Manual/10410-00746W.pdf."""
    
    def __post__(self):
        self.write(':CONFigure:BASe:MODe ANRitsu')
    
    def max_hold(self, trace):
        self.select(trace)
        self.write(f':CALCulate:SELected:MATH:INTErtrace:EQUation "MAX_HOLD( cTr{trace} )"')
        #self.query(':CALCulate:SELected:MATH:INTErtrace:EQUation?')
        self.write(f':CALCulate:SELected:MATH:INTErtrace:STATe {True:b}')

    def max_hold_clear(self, trace):
        self.select(trace)
        self.write(f':CALCulate:SELected:MATH:INTErtrace:STATe {False:b}')

    def smoothing(self, trace, smoothing_percent):
        self.select(trace)
        #self.query_float(':CALCulate:SELected:SMOothing:APERture?')  # Smoothing %
        self.write(f':CALCulate:SELected:SMOothing:APERture {smoothing_percent}')  # Smoothing %

    def smoothing_clear(self, trace, smoothing_percent):
        self.select(trace)
        self.write(f':CALCulate:SELected:SMOothing:APERture {0}')  # Smoothing %
        self.write(f':CALCulate:SELected:SMOothing:STATe {False:b}')  # Smoothing state


    def user_preset(self):
        self.write(f':SENSe{1}:AVERage:COUNt {2}')
        self.write(f':SENSe{1}:AVERage:STATe {False:b}')
        self.write(f':SENSe{1}:AVERage:TYPe POIN')
        self.write(f':SENSe{1}:BANDwidth:RESolution {1e3}')

        for trace in [1, 2, 3, 4]:
            self.select(trace)
            self.write(f':CALCulate:SELected:MATH:INTErtrace:STATe {False:b}')
            self.write(f':CALCulate:SELected:SMOothing:APERture {0}')  # Smoothing %
            self.write(f':CALCulate:SELected:SMOothing:STATe {False:b}')  # Smoothing state

    @property
    def local(self):
        return self.write('RTL')

    @property
    def frequency_start(self):
        """Frequency Start."""
        return self.query_float(':SENSe1:FREQuency:STARt?')

    @frequency_start.setter
    def frequency_start(self, start):
        self.write(f':SENSe1:FREQuency:STARt {start}')

    @property
    def frequency_stop(self):
        """Frequency Stop."""
        return self.query_float(":SENSe1:FREQuency:STOP?")

    @frequency_stop.setter
    def frequency_stop(self, stop):
        self.write(f':SENSe1:FREQuency:STOP {stop}')

    @property
    def sweep_points(self):
        """Sweep Points."""
        return self.query_int(":SENSe1:SWEep:POINt?")

    @sweep_points.setter
    def sweep_points(self, points):
        return self.write(f":SENSe1:SWEep:POINt {points:0.0f}")
            
    @property
    def frequency_axis(self):
        sweep_type = self.query(':SENSe1:SWEep:TYPe?')
        # print(sweeptype)
        start = self.query_float(':SENSe1:FREQuency:STARt?')
        stop = self.query_float(':SENSe1:FREQuency:STOP?')
        step = self.query_int(':SENSe1:SWEep:POINt?')

        if sweep_type == 'LIN':
            return np.linspace(start, stop, step)
        elif sweep_type == 'LOG':
            return np.geomspace(start, stop, step)
        else:
            return None

    def trace(self):
        self.write('FORM:DATA REAL32')
        self.write('FORM:BORD SWAP')

        y = self.query_binary_values(
            ':CALCulate1:DATA:SDATa?',
            container=np.float64
        ).view(np.complex128)

        self.local
        return y
        # plt.plot(x, 20 * np.log10(np.abs(v)))
        # len(v)
        
        
    def trace_formatted(self):
        self.write('FORM:DATA REAL32')
        self.write('FORM:BORD SWAP')

        y = self.query_binary_values(
            ':CALCulate1:DATA:FDATa?',
            container=np.float64
        )

        self.local
        return y
        

    def select(self, parameter=1):
        self.write(f':CALCulate1:PARameter{parameter}:SELect')
        return self.query(f':CALCulate1:PARameter{parameter}:DEFine?')
        # self.query(':CALCulate1:PARameter?')
        # print(x)
        # self.query(':CALCulate1:PARameter:COUNt?')  # 4
        # self.query(':CALCulate1:PARameter1:DEFine?')  # S11
        # self.write(':CALCulate1:PARameter1:SELect')
        # self.write(':CALCulate1:PARameter4:SELect')

    def port_full_two(self):
        data = {}
        define = {}
        for index in 1, 2, 3, 4:
            define[index] = self.select(index)
            data[index] = self.trace()

        df = pd.DataFrame(
            np.column_stack((
                self.frequency_axis,
                data[1].real, data[1].imag,
                data[2].real, data[2].imag,
                data[3].real, data[3].imag,
                data[4].real, data[4].imag,
            )),
            columns=[
                'Frequency (Hz)', 
                f'{define[1]} Real', f'{define[1]} Imag',
                f'{define[2]} Real', f'{define[2]} Imag',
                f'{define[3]} Real', f'{define[3]} Imag',
                f'{define[4]} Real', f'{define[4]} Imag',
            ]
        )
        return df.set_index('Frequency (Hz)')

    def port_single(self, index):
        self.select(index)
        trace = self.trace()

        df = pd.DataFrame(
            np.column_stack((
                self.frequency_axis,
                trace.real, trace.imag,
            )),
            columns=[
                'Frequency (Hz)',
                f'Real', f'Imag',
            ]
        )
        return df.set_index('Frequency (Hz)')
    
    def port_single_formatted(self):
        # self.select(index)
        df = pd.DataFrame(
            np.column_stack((
                self.frequency_axis,
                self.trace_formatted().round(4),
            )),
            columns=[
                'Frequency (Hz)', 
                f'Data (dB)',
            ])

        return df.set_index('Frequency (Hz)')