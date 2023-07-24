from ..IEEE488 import IEEE488
from ..SCPI import SCPI

import numpy as np
import pandas as pd
from datetime import datetime

import PIL.Image as Image
import io
from datetime import datetime

# TODO Mixer setup
# TODO Factors Loading, reading, toggle global, toggle factor (Have external_gain)

class AgilentE44nn(IEEE488, SCPI):

    def __post__(self):
        self.write(f':SYST:ERR:VERB {True:b}')  # Turn on verbose command errors
        # self.OPT = self.SCPI_OPT  # *OPT? is missing from FW
        

    '''    def configure(self):
        self.referenceoutput = True
        self.frequencyspan = 1e3
        self.resolutionbandwidth = 1e3
        # self.write(":RBW 1kHz")
        # self.write(":BAND 1kHz")
        # self.write(":FREQuency:SPAN 1KHz")
    '''
    @property
    def select(self):
        return self.query(':INST:SEL?').strip('"')
    
    @select.setter
    def select(self, mode):
        return self.write(f':INST:SEL {mode}')  # SA, BASIC
    
    @property
    def frequency(self):
        """Center frequency."""
        return self.frequency_center

    @frequency.setter
    def frequency(self, frequency):
        if type(frequency) is list and len(frequency) == 2 and frequency[1] > frequency[0]:  # [1e9, 6e9]
            self.frequency_start = frequency[0]
            self.frequency_stop = frequency[1]
            
        elif type(frequency) is list and len(frequency) == 2 and frequency[1] <= 0:  # [1e9, -3e6], [1e9, 0]
            self.frequency_center = frequency[0]
            self.frequency_span = -frequency[1]
        else:
            self.frequency_center = frequency


            
    @property
    def frequency_center(self):
        """Center frequency."""
        return self.query_float(":FREQuency:CENT?")
    
    @frequency_center.setter
    def frequency_center(self, frequency):
        return self.write(f":FREQuency:CENT {frequency}")
    
    @property
    def frequency_span(self):
        """Frequency Span."""
        return self.query_float(":FREQuency:SPAN?")

    @frequency_span.setter
    def frequency_span(self, span):
        self.write(f':FREQuency:SPAN {span}')
    
    @property
    def frequency_start(self):
        """Frequency Start."""
        return self.query_float(":FREQuency:STARt?")

    @frequency_start.setter
    def frequency_start(self, start):
        self.write(f':FREQuency:STARt {start}')

    @property
    def frequency_stop(self):
        """Frequency Stop."""
        return self.query_float(":FREQuency:STOP?")

    @frequency_stop.setter
    def frequency_stop(self, stop):
        self.write(f':FREQuency:STOP {stop}')

    @property
    def sweep_points(self):
        """Sweep Points."""
        return self.query_int(":SWEep:POINts?")

    @sweep_points.setter
    def sweep_points(self, points):
        # N9030B 1 to 100,001 Zero and non-zero spans
        # E4440A 101 to 8192, 2 to 8192 in zero span
        # [:SENSe]:SWEep:POINts <number of points>
        self.write(f":SWEep:POINts {points:0.0f}")
    
    @property
    def sweep_points_max(self):
        return self.query_int(':SWEep:POINts? MAX')

    @property
    def view_range(self):
        top = self.reference_level
        # self.query_int(':DISP:WIND:TRACE:Y:NDIVision?')
        floor = top - ( 10 * self.query_float(':DISP:WIND:TRACE:Y:PDIVision?'))
        return [top, floor]

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

    def resolution_bandwidths(self):
        rbws = []
        for a in [1e0, 1e1, 1e2, 1e3, 1e4, 1e5]:
            for b in [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]:
                rbws.append(a * b)
        for c in [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3, 4, 5, 6, 8]:
            rbws.append(c * 1e6)
        return np.array(rbws).round(1)
    
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
    def resolution_bandwidth(self, resolutionbandwidth, *, unit='Hz'):
        self.write(f':BANDwidth:RESolution {resolutionbandwidth}')

    @property
    def video_bandwidth(self):
        """Video Bandwidth."""
        # N9030B  1 Hz to 3 MHz (10% steps), 4, 5, 6, 8 MHz
        # N9030B Same as RBW + plus wide-open VBW (labeled 50 MHz)
        value = self.query_float(':BANDwidth:VIDeo?')
        return int(value) if value >= 10 else value

    

    @video_bandwidth.setter
    def video_bandwidth(self, videobandwidth):
        self.write(f':BANDwidth:VIDeo {videobandwidth}')

    _units = {
        'DBM':'dBm',
        'DBMV':'dBmV',
        'DBMA':'dBmA',
        'V':'V',
        'W':'W',
        'A':'A',
        'DBUV':'dBuV',
        'DBUA':'dBuV',
        'DBPW':'dBpW',
        'DBUVM':'dBuV/m',
        'DBUAM':'dBuA/m',
        'DBPT':'dBpT',
        'DBG':'dBG',
    }
    @property
    def unit_power(self):
        """Unit Power."""
        return self._units[self.query(':UNIT:POWer?')]

    @unit_power.setter
    def unit_power(self, unit):
        self.query(f':UNIT:POWer {unit}')

    _detectors = {
        'NORM':'Normal',
        'AVER':'RMS',  # Average / RMS # TODO is this what we think it is?
        'POS':'Positive Peak',
        'SAMP':'Sample',
        'NEG':'Negative PEak',
        'QPE':'Quasi Peak',
        'EAV':'EMI Average',
        'RAV':'RMS Average',
    }
    
    @property
    def detector(self):  # TODO
        return self._detectors[self.query(f':DETector:FUNCtion?')]


    @detector.setter
    def detector(self, detector):
        detectors = dict(map(reversed, self._detectors.items()))
        selected_detector = detectors[detector]
        return self.write(f':DETector:FUNCtion {selected_detector}')

    @property
    def input_attenuator(self):
        return self.query_float(':POWer:RF:ATTenuation?')


    @input_attenuator.setter
    def input_attenuator(self, attenuation):
        return self.write(f':POWer:RF:ATTenuation {attenuation}')
    
    @property
    def continuous(self):
        return self.query_bool(':INIT:CONTinuous?')

    @continuous.setter
    def continuous(self, continuous):
        return self.write(f':INIT:CONTinuous {continuous:b}')
    
    
    @property
    def input_attenuator_auto(self):
        return self.query_bool(':POWer:ATTenuation:AUTO?')


    @input_attenuator_auto.setter
    def input_attenuator_auto(self, state):
        return self.write(f':POWer:ATTenuation:AUTO {state:b}')
    
    _trace_types = {
        'WRIT': 'Clear Write',  # WRITe
        'AVER': 'Trace Average',  # AVERage
        'MAXH': 'Max Hold',  # MAXHold
        'MINH': 'Min Hold',  # MINHold
        # Key to match what analyser returns
    }

    @property
    def trace_type(self):
        return self._trace_types[self.query(f':TRACe{1}:MODE?')]

    @trace_type.setter
    def trace_type(self, type_):
        trace_types = dict(map(reversed, self._trace_types.items()))
        selected_type = trace_types[type_]
        return self.write(f':TRACe{1}:MODE {selected_type}')

    @property
    def external_gain(self):
        return self.query_float(':CORRection:OFFS:MAGN?')


    @external_gain.setter
    def external_gain(self, correction):
        # RF = RF Input
        # EMIXer = External Mixing
        return self.write(f':CORRection:OFFS:MAGN {correction}')
    
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
    
 
    def screenshot(self):
        timeout = self.inst.timeout
        self.inst.timeout = 5000
        if 'TMPIMAGE.GIF' in self.query(":MMEMory:CATalog? \'R:\'"):
            self.write(':MMEMory:DEL \'R:TMPIMAGE.GIF\'')
        # sleep(0.5)

        self.write(':MMEMory:STORe:SCR \'R:TMPIMAGE.GIF\'')
        # sleep(0.5)
        
        image = Image.open(io.BytesIO(
            self.query_binary_values(
                ':MMEMory:DATA? \'R:TMPIMAGE.GIF\'',
                datatype='B', 
                is_big_endian=False, 
                container=bytearray
            )
        ))
        self.inst.timeout = timeout
        return image


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
            'input_attenuator',
            'input_attenuator_auto',
            'sweep_points',
            'unit_power',
            'trace_type',
            'external_gain',
            'view_range'

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
            # This may be inverted WRT most users 0.5 == 2 points per RBW
            # 2 points per RBW min
            df.attrs['points per RBW'] = round(points_per_rbw, 6)  # want <= 1 in most circumstances
            df.attrs['points per RBW_'] = points_per_rbw # want <= 1 in most circumstances

        df.attrs['IDN'] = getattr(self, 'IDN', -1)
        # df.attrs['OPT'] = getattr(self, 'OPT', -1)
        
        now = datetime.now()
        df.attrs['ISO8601'] = now.isoformat()
        df.attrs['YYYYMMDD'] = now.strftime("%Y-%m-%d")
        df.attrs['YYYYMMDDHHMMSS'] = now.strftime("%Y-%m-%d--%H-%M-%S")

        self.local
        return df
        