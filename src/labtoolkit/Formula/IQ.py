from numpy import sqrt, log10, pi, arctan2, average, conj, gradient, angle # arccosh, 
# Prefer numpy over math as handling list/arrays of values works in numpy
# Produces same result for single values

from dataclasses import dataclass

class IQTo:
    """Inphase and Quadrature."""
    # https://pysdr.org/content/sampling.html
    # https://uk.tek.com/blog/quadrature-iq-signals-explained
    # http://whiteboard.ping.se/SDR/IQ
    # https://www.itu.int/dms_pubrec/itu-r/rec/sm/R-REC-SM.2117-0-201809-I!!PDF-E.pdf

    # https://uk.mathworks.com/help/instrument/reading-inphase-and-quadrature-iq-data-from-a-signal-analyzer-over-tcp-ip.html
    # https://en.wikipedia.org/wiki/Complex_number

    @staticmethod
    def Magnitude(data):
        """."""
        # https://www.rohde-schwarz.com/tr/faq/how-to-read-iq-data-from-spectrum-analyzer-and-convert-to-dbm-values-faq_78704-781632.html
        # 3.46423039446e-4, 4.35582856881e-4
        return sqrt(data.real**2 + data.imag**2)

    @classmethod
    def Watts(cls, data):
        """."""
        return cls.Mag(data.real, data.imag)**2 / 50

    @classmethod
    def dBm(cls, data):
        """."""
        # return 10 * log10(cls.Watts(I, Q) / 0.001)
        return 10 * log10(10 * (data.real**2 + data.imag**2))
        # https://www.tek.com/en/blog/calculating-rf-power-iq-samples
        # https://dsp.stackexchange.com/questions/19615/converting-raw-i-q-to-db
        # https://www.pe0sat.vgnet.nl/sdr/iq-data-explained/
        # https://www.rohde-schwarz.com/uk/faq/how-to-read-iq-data-from-spectrum-analyzer-and-convert-to-dbm-values-faq_78704-781632.html

    @staticmethod
    def Phase(data):
        """."""
        return arctan2(data.imag, data.real)  # Phase Angle Rad

    @classmethod
    def Phase_deg(cls, data):
        """."""
        return cls.Phase(data) * 180 / pi  # Phase Angle Deg

    @staticmethod
    def Complex(I, Q):
        """."""
        return I + 1j * Q
    
    @classmethod
    def AM_Demod(cls, data):
        """."""
        mag = cls.Magnitude(data)
        maxima = mag.max()
        minima = mag.min()
        # print(maxima)
        # print(minima)
        avermag = average(mag)

        peak_pos = ((maxima - avermag) / avermag ) * 100
        peak_neg = (-(minima - avermag) / avermag ) * 100
        peak_aver = (peak_pos - -peak_neg) / 2
        peak_peak = ((maxima - minima) / (maxima + minima)) * 100
        
        # R&S AM Mod https://youtu.be/I46eP8uZh_Y?t=182 

        return result_AM_Demod(
            peak_peak.round(2),
            peak_pos.round(2),
            peak_neg.round(2),
            peak_aver.round(2),
        )
        
        # return m.round(6) * 100 # AM Modulation %
    
    @classmethod
    def AM_Demod_with_lowpass(cls, mag):
        """."""
        # mag = cls.Magnitude(data)
        #mag = butter_lowpass_filter(mag, 10e3, fs=50000, order=5)[25:] 
        # return mag
        maxima = mag.max()
        minima = mag.min()
        avermag = average(mag)

        peak_peak = ((maxima - minima) / (maxima + minima)) * 100
        peak_pos = ((maxima - avermag) / avermag ) * 100
        peak_neg = (-(minima - avermag) / avermag ) * 100
        peak_aver = (peak_pos - -peak_neg) / 2
        
        # R&S AM Mod https://youtu.be/I46eP8uZh_Y?t=182 

        return result_AM_Demod(
            peak_peak.round(2),
            peak_pos.round(2),
            peak_neg.round(2),
            peak_aver.round(2),
        )
        
        # return m.round(6) * 100 # AM Modulation %
        
    @classmethod
    def FM_audio_Demod(cls, data):
        """."""
        # IQ = cls.Complex(I, Q)

        # https://witestlab.poly.edu/blog/capture-and-decode-fm-radio/

        # http://witestlab.poly.edu/~ffund/el9043/labs/lab1.html
        # We'll use a kind of frequency discriminator called a polar
        # discriminator. A polar discriminator measures the phase
        # difference between consecutive samples of a
        # complex-sampled FM signal.

        # More specifically, it takes successive complex-valued
        # samples and multiplies the new sample by the conjugate
        # of the old sample. Then it takes the angle of this
        # complex value.

        # This turns out to be the instantaneous frequency
        # of the sampled FM signal.

        rad = data[1:] * conj(data[:-1])  # radians?
        return angle(rad)  # degrees ?
    
        '''
        a = np.arctan2(Q, I)
        b = np.unwrap(2 * a) / 2
        plt.plot(df.index, y)
        '''
        '''
        I = vsl['I'].values
        Q = vsl['Q'].values
        # IQTo.FM_Demod(I, Q)
        IQ = IQTo.Complex(I, Q)
        FM = IQ[1:] * np.conj(IQ[:-1])
        df = pd.DataFrame(np.column_stack((vsl.index[:-1], np.angle(FM))), columns=['Time', 'FM Audio']) 
        df = df.set_index('Time')  
        df[0.00025:0.00025+0.001].plot()
        # IQ
        # IQ
        '''

    '''
    self.i = np.array(self.df['I'])
    self.q = np.array(self.df['Q'])

    def plot_polar(self):
        zoom = np.floor(1 / np.max((self.i, self.q)))

        plt.scatter(self.i*zoom, self.q*zoom, color="red", alpha=0.2)
        plt.title("We can also plot the constellation, which should have the circular pattern typical of an FM signal")
        plt.xlabel("Real")
        plt.xlim(-1.1,1.1)
        plt.ylabel("Imag")
        plt.ylim(-1.1,1.1)

    from handcalcs.decorator import handcalc

    from numpy import arctan2, pi, sin, cos, sqrt, log10, rad2deg, deg2rad


    # negative mag is undefined
    # [trigonometry - Do you ever say that the amplitude is negative? - Mathematics Stack Exchange](https://math.stackexchange.com/questions/804455/do-you-ever-say-that-the-amplitude-is-negative)
    # phase_rad  > +-pi rollover
    # in phase_deg 185 returns 175


    @handcalc(override="long", precision=3, jupyter_display=True)
    def i_from_amplitude_phase(magnitude, phase_rad):
        i = magnitude * cos(phase_rad)  # I
        return i


    @handcalc(override="long", precision=3, jupyter_display=True)
    def q_from_amplitude_phase(magnitude, phase_rad):
        q = magnitude * sin(phase_rad)  # Q
        return q

    '''

@dataclass
class result_AM_Demod:
    """Class for keeping track of an item in inventory."""
    peak_peak: float
    peak_pos: float
    peak_neg : float
    peak_aver: float
    # mag: np.ndarray
