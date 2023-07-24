# from ..GenericInstrument import GenericInstrument
from time import sleep

import numpy as np
import pandas as pd

from ..IEEE488 import IEEE488
from ..SCPI import SCPI

import PIL.Image as Image
import io
from datetime import datetime


class AgilentE4406A(IEEE488, SCPI):
    """."""

    def __post__(self):

        # self.write(':DISPlay:ENABle 1')
        now = datetime.now()

        self.write(f':SYSTem:DATE {now.year},{now.month},{now.day}')
        self.write(f':SYSTem:TIME {now.hour},{now.minute},{now.second}')
        self.write(':DISPlay:ANNotation:CLOCk:DATE:FORMat DMY')
        
        self.write(':SYSTem:ERRor:VERBose 1')
        # self.query('SYSTem:ERRor?')

    '''
    self.write(':SENSe:SPECtrum:AVERage:TYPE LOG')
    self.write(':DISPlay:FORMat:ZOOM')  # :TILE
    self.write(':DISPlay:SPECtrum:WINDow:TRACe:Y:SCALe:PDIVision 10')
    self.write(':DISPlay:SPECtrum:WINDow:TRACe:Y:SCALe:RLEVel -20')
    :INST:SEL BASIC // Set the analyzer in Basic mode
    :FREQ:CENTER xxxMHz // Set center frequency
    :FORM REAL,32 // Set the returned data type to REAL, 32
    :FORM:BORD SWAP // Set the Byte order to Swap
    :INIT:CONT 0 // Set analyzer to single sweep
    :WAV:BWID:RES 300kHz // Set RBW
    :WAV:BAND:TYPE FLAT // Set filter to Flattop
    :CAL:TCOR ON // Turn time corrections on
    :POW:RF:ATT xx // Set attenuation
    :WAV:SWE:TIME xxx // Set sweep time
    :WAV:ACQ:PACK xx // Set data packing if necessary (Only needed for
    RBWs between 1.2 and 7.5 MHz where you need
    more dynamic range, although this may not be
    recommended)
    :READ:WAV0? // Returns the I/Q data
    '''

    @property
    def frequency(self):
        return self.query_float(':SENSe:FREQuency?')

    @frequency.setter
    def frequency(self, frequency):
        self.write(f':SENSe:FREQuency {frequency}')

    @property
    def span(self):
        return self.query_float(':SENSe:SPECtrum:FREQuency:SPAN?')

    @span.setter
    def span(self, frequency):
        self.write(f':SENSe:SPECtrum:FREQuency:SPAN {frequency}')

    @property
    def resbw(self):
        return self.query_float(':SENSe:SPECtrum:BANDwidth:RESolution?')

    @resbw.setter
    def resbw(self, frequency):
        self.write(f':SENSe:SPECtrum:BANDwidth:RESolution {frequency}')
    
    def screenshot(self):
        timeout = self.inst.timeout
        self.inst.timeout = 5000
        image = Image.open(io.BytesIO(
            self.query_binary_values(
                ':HCOPY:SDUMP:DATA? GIF',
                datatype='B', 
                is_big_endian=False, 
                container=bytearray
            )
        ))
        self.inst.timeout = timeout
        return image


    def measure_power_at_marker(self):
        timeout = self.inst.timeout
        self.write('INIT:CONT 0')

        self.inst.timeout = 30 * 1000

        self.write('INIT:IMM')  # states init ignored
        # inst.write('INIT:CONT 0')
        # print(f'Timeout {self.inst.timeout}')

        self.inst.query('*OPC?')
        # print(f'Timeout {self.inst.timeout}')

        # inst.write(f'CALC:SPEC:MARK{1}:MAX')
        # float(inst.query(f'CALC:SPEC:MARK{1}:Y?')), float(inst.query(f'CALC:SPEC:MARK{1}:X?'))
        value = self.query_float(f':CALCulate:SPEC:MARKer{1}:Y?')
        self.inst.timeout = timeout
        # return self.query_float(f'CALC:SPEC:MARK{1}:Y?'))

        return value

    def concatenator(self, start_freq, stop_freq, span=10e6):
        """Concatenates multiple spans of spectrum data taken from the analyser."""
        # self.write(':FORM ASC')
        self.write(':FORM REAL,32')  # Set the returned data type to REAL, 32
        self.write(':FORM:BORD SWAP')  # Set the Byte order to Swap
        line = self.query_binary_values(":READ:SPECtrum1?")
        num_points = int(line[2])  # third field contains the number of points per span
        points_step = float(line[4])  # fifth field contains the frequency step between two points
        # db_per_div = self.query_float(":DISPlay:SPECtrum1:WINDow1:TRACe:Y1:PDIVision?")  # the Y axis reference value in dBm

        # db_ref_value = self.query_float(":DISPlay:SPECtrum1:WINDow1:TRACe:Y1:RLEVel?")  # read back the Y axis reference value in dBm

        # stop_freq, start_freq = 4008e6, 8e6
        total_num_scans = max(1, round((stop_freq - start_freq) / 10e6))  # calculate the number of 10MHz spans required to cover the frequency

        self.write(':INIT:CONT 0')  # Set analyzer to single sweep

        self.inst.timeout = 10e3
        line_nums = []
        df = pd.DataFrame(None, columns=['Hz', 'dBm'])

        for each in tqdm(range(0, total_num_scans)):
            # print(each)
            span = 10e6
            center_freq = start_freq + 0.5 * span + each * span   # calculate the center frequency
            # print(center_freq)
            self.write(f":SENSe:FREQuency:CENTer {center_freq} Hz")     # send the center frequency to the E4406A
            # self.query_bool(':INIT;*OPC?')
            sleep(1)

            # for i in range(0,num_points):    # loop for as many times as there are data points in the span
            # line_nums.extend([(center_freq - (0.5*span) + (i*points_step),round(float(line[i]),2))])
            # add the received span points to the data series as tuples
            y = self.query_binary_values(':READ:SPECtrum4?', container=np.array).round(2)
            cent, span = float(self.query('SENSe:FREQ:CENT?')), float(self.query('SENSe:SPEC:FREQ:SPAN?'))
            # print(cent, span)
            Fl = (- span / 2) + cent
            Fh = (+ span / 2) + cent
            # Fl, Fh
            x = np.linspace(Fl, Fh, len(y))
            dfa = pd.DataFrame(np.column_stack(([x, y])), columns=['Hz', 'dBm'])
            df = df.append(dfa, ignore_index=True)

        return df.set_index('Hz')

    '''
    Hewlett-Packard,E4406A,US41152769,A.10.08    20070628  17:32:45
    :SENSe:SPECtrum:FREQuency:SPAN?:		+1.00000000E+003
    :SENSe:SPECtrum:FREQuency:SPAN?:		+1.00000000E+003
    :SENSe:SPECtrum:BANDwidth:RESolution?:		+4.55000000E-001
    :SENSe:SPECtrum:SWEep:TIME?:		+8.28428813E+000
    :SENSe:SPECtrum:FFT:WINDow:TYPE?:		FLAT
    :SENSe:WAVeform:BANDwidth:RESolution:TYPE?:		GAUS
    :SENSe:POWer:RF:ATTenuation?:		+0
    :SENSe:FREQuency?:		+4.000000000E+009
    :SENSe:SPECtrum:AVERage:TYPE?:		LOG
    :SENSe:SPECtrum:AVERage:STATe?:		1
    :SENSe:SPECtrum:AVERage:COUNt?:		+25
    :SENSe:FEED?:		IFAL
    :SYSTem:ERRor:VERBose 1
    SYSTem:ERRor?:		+0,"No error"
    :DISPlay:ENABle 1
    :SENSe:SPECtrum:FREQuency:SPAN?:		+1.00000000E+003
    :CALC:SPEC:MARK1:Y?:		-2.45338770E+001
    CALC:SPEC:MARK1:X:POS?:		+6759
    :CALCulate:SPEC:MARKer1:TRACe?:		ASP
    :CALCulate:SPEC:MARKer1:X?:		+4.00000000E+009
    4000000000.0
    :FORMat:DATA?:		ASC,+0
    '''
    '''
    :FORM ASC
    :CONF?
    SPEC.
    :INST:SEL?
    BASIC.
    :FETC:SPEC1?
    :SENS:SPEC:BAND:RES?
    +4.67000000E+002
    :SENS:SPEC:SWE:TIME?
    +8.04440000E-003
    :SENSe:FREQ:CENT?
    +5.00000000E+007
    :SENSe:SPEC:FREQ:SPAN?
    +1.00000000E+003
    :INIT:CONT?
    :FORM REAL, 32
    :FETCH:SPEC4?
    :FORM ASC
    INIT:CONT ON;
    '''

    @property
    def rfgain(self):
        return self.query_float(':CORR:LOSS?')

    @rfgain.setter
    def rfgain(self, rfgain):
        self.write(f':CORR:LOSS {rfgain}')

    @property
    def resbw_ratio(self):
        return self.resbw * self.aper

    @property
    def decim(self):
        return round(1.0 / (self.resbw * self.aper))

    @property
    def decimated_bw(self):
        return (1.0 / self.aper) / self.decim

    @property
    def resbw(self):
        return self.query_float(':WAV:BWID?')

    @resbw.setter
    def resbw(self, resbw):
        self.write(f':WAV:BWID {resbw}')
        # set resolution bandwidth
        # d_resbw = value_d  # update with value as set by the instrument

    @property
    def aper(self):  # Sample rate
        return self.query_float(':WAV:APER?')

    @aper.setter
    def aper(self, aper):
        self.write(f'APER {aper}')

    @property
    def time(self):
        self.query_float(':WAV:SWE:TIME?')

    @time.setter
    def time(self, time):
        self.write(f':WAV:SWE:TIME {time}')

    # :FREQ:CENT
    @property
    def stateiq(self):
        return {
            'Resolution BW': self.resbw,
            'RBW ratio': self.resbw_ratio,
            'Decimation': self.decim,
            'Sample Rate': self.aper,
            'Span decimated': self.decimated_bw,
            'Sweep time': self.time,
            'Center': self.frequency,
            'Center (MHz)': self.frequency / 1e6,
        }

    def iqinit(self):
        self.write(":INST:NSEL 8;:CONF:WAV")  # config for I/Q output
        self.write(":INIT:CONT 0;:FORM:BORD SWAP;:FORM REAL, 32;:WAV:BWID:TYPE FLAT;:CAL:TCOR ON;:CAL:AUTO ALERT;:STAT:OPER:ENAB 32")  # other settings
        self.write(":SYST:KLOC 1")  # inhibit keyboard
        self.write(":SYST:MESS \"In Use by GNU Radio - front panel disabled\"")  # send informatory message to E4406A status line
        self.write(":DISP:ENAB 0")  # inhibit display

    def iqrelease(self):
        self.write(":DISP:ENAB 1")  # release display
        self.write(":SYST:KLOC 0")  # release keyboard
        self.write(":INIT:CONT 1")  # restore continuous measurement
        # self.write(":CAL:AUTO ON")  # restore auto calibration
    def iq(self):
      
        self.write(':FORM REAL,32')  # Set the returned data type to REAL, 32
        self.write(':FORM:BORD SWAP')  # Set the Byte order to Swap
                
        # self.query_binary_values(':READ:WAV0?')
        IQ = self.inst.query_binary_values(":FETCh:SPECtrum3?", container=np.float64).view(np.complex128)

        t = np.linspace(0, self.query_float(':SENSe:SPECtrum:SWEep:TIME?'), len(IQ))

        df = pd.DataFrame(
            np.column_stack((t, IQ.real, IQ.imag)), 
            columns=['S', 'I', 'Q']
        ).set_index('S')
        
        
        df.attrs['Time Stamp'] = 'Now'
        
        params = [
            'IDN'
            'frequency', 
            'resbw', 
            'span',
            'resbw_ratio',
            'decim',
            'aper',
            'decimated_bw',
            'time',
        ]
        
        for param in sorted(params):
            df.attrs[param] = getattr(self, param, -1)

        
        return df

    '''
    @property
    def iq(self):

        self.write(':FORMat REAL,32')
        self.write(':FORMat:BORDer SWAPped')
        self.inst.timeout = 20000
        # IQ = self.query_binary_values(':Fetch:SPECtrum0?', container=np.array)  # .view(np.complex)  # Fetch

        IQ = self.query_binary_values(':READ:WAV0?', container=np.array)  # .view(np.complex)  # Fetch
        # d_sweep_time = d_samp_rate * (d_nb_points - 1) * d_block_factor;
        # size_t actual_nb_points = ((sweep_time/d_samp_rate)+2);
        # actual_nb_points = ((sweep_time/d_samp_rate)+2);

        I, Q = IQ[0::2], IQ[1::2]
        #  0 index and 1 index then 2 is every other value in the array
        # IQComplex = I + 1j*Q

        return I, Q
    '''
    def MeasureIQ(self):
        """."""
        # generator = FunctionName(inst)
        # Inital call of next(generator) runs the init/setup, when next is called the first time
        # RST ?
        self.iqinit()

        # Using next(generator) and subsequent calls to next(generator) yields a measurement

        # A subsequent call to the generator.send() allows input of infomation to the generator
        # The input of the generator.send(input) will be the result of the yield statement
        # x in this case

        x = None  # Using None allows you to not have to use generator.send(None) when you don't have data to input
        # This allows for a not None to be used as a flow control

        while x is None:
            x = yield self.iq

        # When x is set to anything other than None, and the while loop finishes in that state this (↓) will be reached
        self.iqrelease()  # Free run
        yield False

    def trace(self):
        self.write(':FORMat REAL,32')
        self.write(':FORMat:BORDer SWAPped')

        data = self.inst.query_binary_values(':FETCh:SPECtrum4?', container=np.array)  # Fetch
        center = self.query_float(':SENSe:FREQuency:CENTer?')
        span = self.query_float(':SENSe:SPECtrum:FREQuency:SPAN?')
        frequencies = np.linspace((center - 0.5 * span), (center + 0.5 * span), len(data))

        # return frequencies, data

        return pd.DataFrame(
            np.column_stack((frequencies, data)),
            columns=['Hz', 'dBm']
        ).set_index('Hz')
        # df['dBm'] = np.clip(df['dBm'], -130, 400)
        # return df



    def VOID(self):
        """
        Void.
        # inst.write(f'CALC:SPEC:MARK{1}:TRAC ASP')
        inst.write(f'CALC:SPEC:MARK{1}:MAX')
        float(inst.query(f'CALC:SPEC:MARK{1}:Y?')), float(inst.query(f'CALC:SPEC:MARK{1}:X?'))
        inst.write(f'SENSe:FREQ:CENT {1e9+200} HZ')
        # y = np.array(inst.query_binary_values(':FETC:SPEC4?'))  # .view(np.complex)
        # y = np.array()  # TRACE:DATA? TRACE1
        print(inst.write(w))
        inst.timeout = 12000
        yref = inst.query_binary_values(':FETC:SPEC4?', container=np.array)
        # y = np.array(inst.query_ascii_values(':READ:SPECtrum4?'))  # TRACE:DATA? TRACE1
        cent, span = float(inst.query('SENSe:FREQ:CENT?')), float(inst.query('SENSe:SPEC:FREQ:SPAN?'))
        state = inst.query(':FETCh:SPECtrum1?').strip().split(',')
        # print(len(state))
        # pprint(state)
        FFTPeak, FFTPeakFrequency, FFTpoints, FirstFFTFrequency, FFTspaceing, Timedomainpoints,
        TimeFirsttimepoint, Timespaceing, TimeComplexOrRaw, ScanTime, CurrentAverageCount = state
        # self.write('*CLS')
        # values = inst.query_ascii_values(':FETCh:SPECtrum7?', container=np.array)
        print(float(FirstFFTFrequency)+float(inst.query(':SENSe:SPECtrum:FREQuency:SPAN?')))
        x = np.around(np.linspace(float(FirstFFTFrequency), float(FirstFFTFrequency)+stop, int(FFTpoints)), decimals=2)
        # if inst.query(':CONFigure?') == 'SPEC':
        # pprint(values)
        # print(len(values))
        self.query(':SENSe:SPECtrum:FREQuency:SPAN?')
        # [:SENSe]:ROSCillator:SOURce INTernal|EXTernal
        # [:SENSe]:ROSCillator:OUTPut[:STATe] OFF|ON|0|1
        # [:SENSe]:ROSCillator:EXTernal:FREQuency?
        # [:SENSe]:FEED RF|IQ|IONLy|QONLy|AREFerence|IFALign
        # [:SENSe]:CORRection[:RF]:LOSS?
        # :SYSTem:VERSion?
        timeout = inst.timeout
        inst.timeout = 60000
        # :CALibration:DISPlay:LEVel OFF|LOW|HIGH
        print(inst.query(':CALibration:ALL?'))
        inst.timeout = timeout
        # self.query(':CALibration:DISPlay:LEVel?')
        # self.query(':SENSe:SPECtrum:TRIGger:SOURce?')  # EXTernal[1]|EXTernal2|FRAMe|IF|LINE|IMMediate|RFBurst
        # inst.write('SENSe:FREQuency {}'.format(2.437e9))
        self.query(':SENSe:SPECtrum:FREQuency:SPAN?')  # Span
        #  {}'.format(10e6))
        self.query(':SENSe:SPECtrum:BANDwidth:RESolution?')  # RBW (Hz)
        # [:SENSe]:SPECtrum:BANDwidth|BWIDth[:RESolution]:AUTO?
        self.query(':SENSe:SPECtrum:SWEep:TIME?')  # Seconds
        self.query(':SENSe:SPECtrum:FFT:WINDow:TYPE?')  # BH4Tap|BLACkman|FLATtop|GAUSsian|HAMMing|HANNing|KB70|KB90|KB110|UNIForm
        self.query(':SENSe:WAVeform:BANDwidth:RESolution:TYPE?')  # FLATtop|GAUSsian
        # self.query(':SENSe:SPECtrum:FFT:WINDow:LENGth?')
        self.query(':SENSe:POWer:RF:ATTenuation?')  # POW:ATT 40dB
        self.query(':SENSe:FREQuency?')  # +2.25648000E+008
        # inst.write('SENSe:FREQuency {}'.format(225.648e6))
        self.query(':SENSe:SPECtrum:AVERage:TYPE?')  # LOG|MAXimum|MINimum|RMS|SCALar
        self.query(':SENSe:SPECtrum:AVERage:STATe?')
        self.query(':SENSe:SPECtrum:AVERage:COUNt?')
        # [:SENSe]:SPECtrum:AVERage:CLEar
        self.query(':SENSe:FEED?')  # RF|IQ|IONLy|QONLy|AREFerence|IFALign
        self.write(':SENSe:FEED AREF')
        self.write(':SENSe:FREQuency 50e6')
        self.write(':SENSe:SPECtrum:FREQuency:SPAN 1e3')
        self.write(':SENSe:SPECtrum:BANDwidth:RESolution 553')  # RBW (Hz)
        self.write(':SENSe:SPECtrum:AVERage:TYPE LOG')
        self.write(':DISPlay:FORMat:ZOOM')  # :TILE
        self.write(':DISPlay:SPECtrum:WINDow:TRACe:Y:SCALe:PDIVision 10')
        self.write(':DISPlay:SPECtrum:WINDow:TRACe:Y:SCALe:RLEVel -20')
        values = inst.query_ascii_values(':FETCh:SPECtrum7?', container=np.array)
        pprint(values)
        # self.query(':SENSe:SPECtrum:FREQuency:SPAN?')
        # print(float(FirstFFTFrequency)+float(self.query(':SENSe:SPECtrum:FREQuency:SPAN?')))
        # cen = float(inst.query(':SENSe:FREQuency?'))
        # halfspan = float(inst.query(':SENSe:SPECtrum:FREQuency:SPAN?')) / 2
        print(float(FirstFFTFrequency))
        stop = float(FFTspaceing) * (int(FFTpoints)-1)
        x = np.linspace(float(FirstFFTFrequency), float(FirstFFTFrequency)+stop, int(FFTpoints), dtype=np.int32)
        x = np.rint(np.linspace(float(FirstFFTFrequency), float(FirstFFTFrequency)+stop, int(FFTpoints)))
        pprint(x)
        x = np.around(np.linspace(float(FirstFFTFrequency), float(FirstFFTFrequency)+stop, int(FFTpoints)), decimals=1)
        print(x)
        # self.write('CALC:SPEC:MARK1:X:POS 13516')
        # self.write(':CALCulate:SPECtrum:MARKer:MAXimum')
        self.query(':CALC:SPEC:MARK1:Y?')
        # self.query(':CALCulate:SPECtrum:MARKer 1:X:POSition?')
        self.query('CALC:SPEC:MARK1:X:POS?')
        self.query(':CALCulate:SPEC:MARKer1:TRACe?')
        # :CALCulate:<measurement>:MARKer[1]|2|3|4[:STATe] OFF|ON|0|1  # CALC:SPEC:MARK2: on
        print(float(self.query(':CALCulate:SPEC:MARKer1:X?')))
        # :CALCulate:<measurement>:MARKer:AOFF
        # :DISPlay:ENABle OFF
        # self.write(':FORMat:DATA REAL,64')
        self.query(':FORMat:DATA?')
        """
        return NotImplemented