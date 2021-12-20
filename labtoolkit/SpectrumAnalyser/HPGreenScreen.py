import numpy as np
import pandas as pd

from ..Instrument import Instrument
from .SpectrumAnalyser import ABCSpectrumAnalyser

class HPGreenScreen(Instrument, ABCSpectrumAnalyser):  # Analyser


    # inst.write('CLRW TRA')  # Clear Write Trace A
    # inst.write('MXMH TRA')  # Max Hold Trace A
    # 'PWRUPTIME?'
    
    @property
    def frequency_start(self):
        """."""
        return self.query_float('FA?')

    @frequency_start.setter
    def frequency_start(self, start):
        self.write(f'FA {start} Hz')
        
    @property
    def frequency_center(self):
        """."""
        return self.query_float('CF?')  ## TODO TBC

    @frequency_center.setter
    def frequency_center(self, center):
        self.write(f'CF {center} Hz')
        
    @property
    def frequency_stop(self):
        """."""
        return self.query_float('FB?')

    @frequency_stop.setter
    def frequency_stop(self, stop):
        self.write(f'FB {stop} Hz')
   
    @property
    def frequency_span(self):
        """."""
        return self.query_float('SP?')

    @frequency_span.setter
    def frequency_span(self, span):
        self.write(f'SP {span} Hz')

    @property
    def sweep_time(self):
        """Sweep Time."""
        return self.query_float("ST?")

    @sweep_time.setter
    def sweep_time(self, time):
        if time == -1:
            self.write(f'ST AUTO')
        else:
            self.write(f"ST {time}s")
    
    @property
    def reference_level(self):
        """Reference level."""
        return self.query_float('RL?')

    @reference_level.setter
    def reference_level(self, level):
        self.write(f'RL {level} DB')

    def resolution_bandwidths(self):
        arr = np.array(
            [1e3, 3e3, 10e3, 30e3, 100e3, 300e3, 1e6, 3e6]
        ).round(1)
        # if EMC [, 9e3, 120e3]
        # if EMC and 200 Hz [200]
        return arr
    
    @property
    def resolution_bandwidth(self):
        """Resolution Bandwidth."""
        value = self.query_float('RB?')
        return int(value) if value >= 10 else value
            
    @resolution_bandwidth.setter
    def resolution_bandwidth(self, resolution_bandwidth):
        if resolution_bandwidth == -1:
            self.write('RB AUTO')
        else:
            self.write(f'RB {resolution_bandwidth} Hz')
        
    @property
    def video_bandwidth(self):
        """Video Bandwidth."""
        value = self.query_float('VB?')
        return int(value) if value >= 10 else value

    @video_bandwidth.setter
    def video_bandwidth(self, video_bandwidth):
        if video_bandwidth == -1:
            self.write('VB AUTO')
        else:
            self.write(f'VB {video_bandwidth} Hz')

    @property
    def amplitude(self):
        """."""
        self.write('MKPK HI')
        return self.query_float('MKA?')

    @property
    def trace(self):
        y = self.inst.query_ascii_values('TRA?', container=np.array)
        if self.frequency_span == 0.0:
            df = pd.DataFrame(
                np.column_stack((
                    np.linspace(0, self.sweep_time, len(y)), y
                )), 
                columns=['Time (s)', 'dBm']  # TODO Unit Power
            )
            return df.set_index('Time (s)')
        else:
            x = np.linspace(self.frequency_start, self.frequency_stop, len(y))
            df = pd.DataFrame(
                np.column_stack((x, y)), 
                columns=['Frequency (Hz)', 'dBm']  # TODO Unit Power
            )
            return df.set_index('Frequency (Hz)')



        # plt.plot(*analyser.trace)
        # pd.DataFrame(np.column_stack((sa.trace)), index=None, columns=['Frequency', 'Amplitude'])
        # pd.DataFrame(np.column_stack((sa.trace)), index=None, columns=['Frequency (Hz)', 'Amplitude (dBm)']).set_index('Frequency (Hz)').plot()

'''
common = "MXRMODE INT;AMPCOR ON;FREF EXT;"
common2 = "MXRMODE EXT;EXTMXR UNPR;"
lists = [
    ["6-12.4GHz", common + "FA 6000MHZ;FB 12400MHZ"],
    ["6-18GHz", common + "FA 6000MHZ;FB 18000MHZ"],
    ["12.4-18GHz", common + "FA 12400MHZ;FB 18000MHZ"],
    ["18-24GHz", common + "FA 18000MHZ;FB 24000MHZ"],
    ["18-26.5Hz", common + "FA 18000MHZ;FB 24000MHZ"],
    ["Measure 310.7MHz", common + "CF 310.7MHZ;SP 10MHZ"],
    ["Band K 18.0 to 26.5GHz", common2 + "FULBAND K;"],
    ["Band A 26.5 to 40.0GHz", common2 + "FULBAND A;"],
    ["Band Q 33.0 to 50.0GHz", common2 + "FULBAND Q;"],
    ["Band U 40.0 to 60.0GHz", common2 + "FULBAND U;"],
    ["Band V 50.0 to 75.0GHz", common2 + "FULBAND V;"],
    ["Band E 60.0 to 90.0GHz", common2 + "FULBAND E;"],
    ["Band W 75.0 to 110.0Hz", common2 + "FULBAND W;"],
    ["Band F 90.0 to 140.0GHz", common2 + "FULBAND F;"],
    ["Band D 110.0 to 170.0GHz", common2 + "FULBAND D;"],
    ["Band G 140.0 to 220.0GHz", common2 + "FULBAND G;"],
    ["Band Y 170.0 to 260.0GHz", common2 + "FULBAND Y;"],
    ["Band J 220.0 to 325.0GHz", common2 + "FULBAND J;"],
    
    ]
'''