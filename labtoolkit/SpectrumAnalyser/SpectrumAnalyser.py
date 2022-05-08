import abc


class ABCSpectrumAnalyser(metaclass=abc.ABCMeta):
    
    @property
    def frequency(self):
        """Center frequency."""
        return self.frequency_center

    @frequency.setter
    def frequency(self, frequency):
        if type(frequency) is list and len(frequency) == 2 and frequency[1] > 0:
            # [1e9, 6e9]  # 1 to 6 GHz
            self.frequency_start = frequency[0]
            self.frequency_stop = frequency[1]
        elif type(frequency) is list and len(frequency) == 2 and frequency[1] <= 0:  
            # [1e9, -3e6]  # 3 MHz span at 1 GHz
            # [1e9, 0]  # Zero Span
            self.frequency_center = frequency[0]
            self.frequency_span = -frequency[1]
        else:
            # 1e9  # 1 GHz
            self.frequency_center = frequency

    @property
    @abc.abstractmethod
    def frequency_center(self):
        """Center frequency."""
        return self.query_float(":FREQuency:CENT?")
    
    @frequency_center.setter
    def frequency_center(self, frequency):
        return self.write(f":FREQuency:CENT {frequency}")
    
    @property
    @abc.abstractmethod
    def frequency_span(self):
        """Frequency Span."""
        return self.query_float(":FREQuency:SPAN?")

    @frequency_span.setter
    def frequency_span(self, span):
        self.write(f':FREQuency:SPAN {span}')
    @property
    @abc.abstractmethod
    def frequency_start(self):
        """Frequency Start."""
        return self.query_float(":FREQuency:STARt?")

    @frequency_start.setter
    def frequency_start(self, start):
        self.write(f':FREQuency:STARt {start}')

    @property
    @abc.abstractmethod
    def frequency_stop(self):
        """Frequency Stop."""
        return self.query_float(":FREQuency:STOP?")

    @frequency_stop.setter
    def frequency_stop(self, stop):
        self.write(f':FREQuency:STOP {stop}')

    @property
    @abc.abstractmethod
    def sweep_time(self):
        """Sweep Time."""
        return self.query_float(":SWEep:TIME?")

    @sweep_time.setter
    def sweep_time(self, time):
        if time == -1:
            self.write(f':SWEep:TIME:AUTO {True:b}')
        else:
            self.write(f":SWEep:TIME {time}")
    
    @property
    @abc.abstractmethod
    def reference_level(self):
        """Reference level."""
        return self.query_float(':DISP:WIND:TRACE:Y:RLEV?')

    @reference_level.setter
    def reference_level(self, lvl):
        self.write(f':DISP:WIND:TRACE:Y:RLEV {lvl}')

    @property
    @abc.abstractmethod
    def resolution_bandwidth(self):
        """Resolution Bandwidth."""
        value = self.query_float(':BANDwidth:RESolution?')
        return int(value) if value >= 10 else value
            
    @resolution_bandwidth.setter
    def resolution_bandwidth(self, resolution_bandwidth):
        self.write(f':BANDwidth:RESolution {resolution_bandwidth}')
        # TODO -1 for auto

    @property
    @abc.abstractmethod
    def video_bandwidth(self):
        """Video Bandwidth."""
        value = self.query_float(':BANDwidth:VIDeo?')
        return int(value) if value >= 10 else value

    @video_bandwidth.setter
    def video_bandwidth(self, video_bandwidth):
        self.write(f':BANDwidth:VIDeo {video_bandwidth}')
        # TODO -1 for auto

class SCPISpectrumAnalyser(ABCSpectrumAnalyser):

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

'''        
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
    def reference_output(self):
        """10MHz output."""
        return self.query_bool(':SENSe:ROSCillator:OUTPUT?')

    @reference_output.setter
    def reference_output(self, boolean=True):
        self.write(f':SENSe:ROSCillator:OUTPUT:STATe {boolean:b}')

def _resolution_bandwidths(self):
        rbws = []
        for a in [1e0, 1e1, 1e2, 1e3, 1e4, 1e5]:
            for b in [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]:
                rbws.append(a * b)
        for c in [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3, 4, 5, 6, 8]:
            rbws.append(c * 1e6)
        return np.array(rbws).round(1)
    

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
    def detector(self):
        return self._detectors[self.query(f':DETector:TRACe{1}?')]


    @detector.setter
    def detector(self, detector):
        detectors = dict(map(reversed, self._detectors.items()))
        selected_detector = detectors[detector]
        return self.write(f':DETector:TRACe{1} {selected_detector}')

    @property
    def input_attenuator(self):
        return self.query_int(':POWer:ATTenuation?')


    @input_attenuator.setter
    def input_attenuator(self, attenuation):
        return self.write(f':POWer:ATTenuation {attenuation}')
    
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

    @property
    def external_gain(self):
        return self.query_float(':CORRection:SA:GAIN?')


    @external_gain.setter
    def external_gain(self, correction):
        # RF = RF Input
        # EMIXer = External Mixing
        return self.write(f':CORRection:SA:GAIN {correction}')
    
    
    @property
    def trace(self):
        return NotImplemented
        
'''