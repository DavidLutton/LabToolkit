from ..IEEE488 import IEEE488
from ..SCPI import SCPI

import numpy as np
import pandas as pd
from datetime import datetime as dt
from .SpectrumAnalyser import SCPISpectrumAnalyser

import PIL.Image as Image
import io


class RaSESW(IEEE488, SCPI, SCPISpectrumAnalyser):

    def __post__(self):
        # self.write(f':SYST:ERR:VERB {True:b}')  # Turn on verbose command errors
        # now = dt.now()
        # self.write(f':SYST:DATE "{now:%Y},{now:%m},{now:%d}"')
        # self.write(f':SYST:TIME "{now:%H},{now:%M},{now:%S}"')
        # ^ not available in other modes eg BASIC
        self.local

    @property
    def select(self):
        return self.query(':INST:SEL?')
    
    @select.setter
    def select(self, mode):
        return self.write(f':INST:SEL {mode}')  # SA, BASIC, ...
    
    @property
    def sweep_points(self):
        """Sweep Points."""
        return self.query_int(":SWEep:POINts?")

    @sweep_points.setter
    def sweep_points(self, points):
        self.write(f":SWEep:POINts {points:0.0f}")
    

    @property
    def sweep_time(self):
        """Sweep Time."""
        '''Replace <meas> with the meas name, eg CHPower
        [:SENSe]:<meas>:SWEep:TIME <time>
        [:SENSe]:<meas>:SWEep:TIME?
        [:SENSe]:<meas>:SWEep:TIME:AUTO OFF|ON|0|1
        [:SENSe]:<meas>:SWEep:TIME:AUTO?
        '''
        return self.query_float(":SWEep:TIME?")

    @sweep_time.setter
    def sweep_time(self, time):
        if time == -1:
            self.write(f':SWEep:TIME:AUTO {True:b}')
        else:
            self.write(f":SWEep:TIME {time}")


    @property
    def reference_level(self):
        """Reference level."""
        # N9030B Log scale –170 to +30 dBm in 0.01 dB steps
        # N9030B Linear scale 707 pV to 7.07 V with 0.11% (0.01 dB) resolution
        return self.query_float(':DISP:WIND:TRACE:Y:RLEV?')

    @reference_level.setter
    def reference_level(self, lvl):
        self.write(f':DISP:WIND:TRACE:Y:RLEV {lvl}')
        # used for seting reference level to a reasonable amount above the measured value
        # and therefor prevent recording clipped values


    @property
    def resolution_bandwidth(self):
        """Resolution Bandwidth."""
        # N9030B 1 Hz to 3 MHz (10% steps), 4, 5, 6, 8 MHz
        # N9030B Bandwidths 1 Hz to 3 MHz are spaced at 10% spacing using
        # the E24 series (24 per decade):
        # 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6,
        # 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1 in each decade
        value = self.query_float(':BANDwidth:RESolution?')
        return int(value) if value >= 10 else value
            
    @resolution_bandwidth.setter
    def resolution_bandwidth(self, resolution_bandwidth):
        self.write(f':BANDwidth:RESolution {resolution_bandwidth}')

    @property
    def video_bandwidth(self):
        """Video Bandwidth."""
        # N9030B  1 Hz to 3 MHz (10% steps), 4, 5, 6, 8 MHz
        # N9030B Same as RBW + plus wide-open VBW (labeled 50 MHz)
        value = self.query_float(':BANDwidth:VIDeo?')
        return int(value) if value >= 10 else value

    

    @video_bandwidth.setter
    def video_bandwidth(self, video_bandwidth):
        self.write(f':BANDwidth:VIDeo {video_bandwidth}')

  
    @property
    def trace_data(self):
        # :INST:SEL?
        # SA
        
        # self.query(':DISP:WIND:TRAC:Y:RLEV?')  # -1.000E+01
        # self.query(':DISP:WIND:TRAC:Y:SPAC?')  # LOG.
        # self.query(':DISP:WIND:TRAC:Y:SCAL:PDIV?')  # +1.000E+01
        
        self.write('FORM:DATA REAL,32')
        self.write('FORM:BORD SWAP')
        return self.inst.query_binary_values(f'TRAC:DATA? TRACE{1}', container=np.float64)
    
    
    @property
    def trace(self):
        if self.select == 'SA':
            return self.trace_sa
        
        # if self.select == 'BASIC':
        #    return self.trace_vsa
        
    @property
    def trace_sa(self):
        type_ = 'Time' if self.frequency_span == 0.0 else 'Frequency'

        if type_ == 'Frequency':
            df = pd.DataFrame(
                np.column_stack((
                    np.linspace(
                        self.frequency_start, 
                        self.frequency_stop, 
                        self.sweep_points,
                    ), 
                    self.trace_data)), 
                columns=['Frequency (Hz)', f'Power ({self.unit_power})'],
            ).set_index('Frequency (Hz)')
            
        if type_ ==  'Time':
            df = pd.DataFrame(
                np.column_stack((
                    np.linspace(
                        0,  # TODO Could have hold off, index to zero anyway?
                        self.sweep_time, 
                        self.sweep_points,
                    ), 
                    self.trace_data
                )),
                columns=['Time (s)', f'Power ({self.unit_power})'],
            ).set_index('Time (s)')
            
        params = [
            'sweep_time', 
            'resolution_bandwidth', 
            'video_bandwidth',
            'reference_level',
            'frequency_span',
            'frequency_start',
            'frequency_stop',
            'frequency',
            # 'detector',
            # 'input_attenuator',
            # 'input_attenuator_auto',
            'sweep_points',
            'unit_power',
            # 'trace_type',
            # 'feed',
            # 'external_gain',
            
            
            # Segment
            # Average Count
            # Average Type
            # RBW
            # RBW Filter
            # RBW Filter BW
            # Sweep Type Swept / FFT
            # X Axis Scale
            # PreAmp State
            # PreAmp Band
            # Trigger Source
            # Trigger Level
            # Trigger Slope
            # Trigger Delay
            # Phase Noise Optimization
            # Swept If Gain
            # FFT If Gain
            # RF Coupling
            # FFT Width
            # Ext Ref
            # RF Calibrator
            # Ref Level Offset
            # Trace Math
            # Trace Math Oper1
            # Trace Math Oper2
            # Trace Math Offset
            # Normalize
            # Trace Name
            # X Axis Units
            # Y Axis Units
        ]
        
        for param in sorted(params):
            df.attrs[param] = getattr(self, param, -1)

        if type_ == 'Frequency':
            points_per_rbw = \
                self.frequency_span / self.sweep_points / self.resolution_bandwidth
            df.attrs['points per RBW'] = round(points_per_rbw, 6)  # want <= 1 in most circumstances
            df.attrs['points per RBW_'] = points_per_rbw # want <= 1 in most circumstances

        df.attrs['IDN'] = getattr(self, 'IDN', -1)
        df.attrs['OPT'] = getattr(self, 'OPT', -1)
        
        now = dt.now()
        df.attrs['ISO8601'] = now.isoformat()
        df.attrs['YYYYMMDD'] = now.strftime("%Y-%m-%d")
        df.attrs['YYYYMMDDHHMMSS'] = now.strftime("%Y-%m-%d--%H-%M-%S")

        self.local
        return df
        