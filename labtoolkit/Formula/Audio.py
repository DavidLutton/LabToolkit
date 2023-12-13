"""Calculate various audio filters inc A-weighting filter."""

# from https://en.wikipedia.org/wiki/A-weighting#Function_realisation_of_some_common_weightings

import numpy as np


class Aweighting():
    def internal(self, f):
        return ( 12194**2 * f**4 ) / (
            (f**2 + 20.6**2) * 
            np.sqrt(
                (f**2 + 107.7**2) * (f**2 + 737.9**2)
            )
            * (f**2 + 12194**2)
        ) 
    
    def filter(self, f):
        return 20*np.log10(self.internal(f))- 20*np.log10(self.internal(1000))

class Bweighting():
    def internal(self, f):
        return ( 12194**2 * f**3 ) / (
            (f**2 + 20.6**2) * 
            np.sqrt(
                (f**2 + 158.2**2) 
            )
            * (f**2 + 12194**2)
        ) 
    
    def filter(self, f):
        return 20*np.log10(self.internal(f))- 20*np.log10(self.internal(1000))

class Cweighting():
    def internal(self, f):
        return ( 12194**2 * f**2 ) / (
            (f**2 + 20.6**2) * (f**2 + 12194**2)
        )
    
    def filter(self, f):
        return 20*np.log10(self.internal(f)) + 0.06

class Dweighting():
    def filter(self, f):
       a = f/(6.8966888496476e-5)
       h = ((1037918.48 - f**2)**2 + (1080768.16* f**2))/((9837328 - f**2)**2 + (11723776*f**2))
       b = np.sqrt(
           h/((f**2 + 79919.29) * (f**2 + 1345600.0))
       )
       return 20*np.log10(a*b)

class Zweighting():
    def filter(self, f):
       return 0  # there are discussions that this should have defined high & low pass filtering
       # Z Weighting
       # https://www.noisemeters.co.uk/help/faq/frequency-weighting/




class ITU_R468noiseweighting():
    """CCIR 468 Weighting (ITU-R 468)."""
    def filter(self, f):
        h1 = -4.737338981378384e-24 *  f**6 + 2.043828333606125e-15 * f**4 - 1.363894795463638e-7 * f**2 + 1
        h2 = 1.306612257412824e-19 * f**5 - 2.118150887518656e-11 * f**3 + 5.559488023498642e-4 * f
    
        R_ITU = 1.246332637532143e-4 * f / np.sqrt(h1**2 + h2**2)
        return 18.2 + 20 * np.log10(R_ITU)



# xa = np.linspace(20, 30e3, 2999)
# ya = IEC179Aweighting().filter(xa)






import numpy as np
import scipy.constants as constants
from scipy import signal

import sounddevice as sd



# audio.play(audio.tones.boop() * 0.25)

class tones:
    
    sample_rate = 44100  # The sampling sample_rate in Hz (should be twice the Nyquist frequency)
    
    @classmethod
    def items(self):
        # keys = [x for x in dir(self) if x.startswith('tone_')] 
        keys = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__") and not func=='items']
        values = [getattr(self, keys) for keys in keys]
        return dict(zip(keys, values)).items()
        
    @staticmethod
    def progress():
        frequency = 440
        duration = 0.3
        time = np.linspace(0., duration, int(sample_rate * duration))
        waveform = \
            1.0 * np.sin(frequency * np.pi * time) + \
            1.0 * np.sin(frequency * constants.golden * np.pi * time)
        return waveform * 0.5

    @staticmethod
    def marginal():
        frequency = 640
        duration = 0.3
        time = np.linspace(0., duration, int(sample_rate * duration))

        waveform = \
            1.0 * np.sin(frequency * np.pi * time) + \
            0.3 * np.sin(3.6 * frequency * np.pi * time) + \
            0.3 * np.sin(4.2 * frequency * np.pi * time)
        return waveform * 0.4

    @staticmethod
    def negative():
        frequency = 440
        duration = 0.3
        time = np.linspace(0., duration, int(sample_rate * duration))

        waveform = \
            0.8 * signal.sawtooth(frequency * np.pi * time) + \
            1.0 * np.sin(frequency * np.pi * time)
        return waveform * 0.25

    @staticmethod
    def carry_on():  # was next but reserverd word 
        # fs = 44100  # sampling sample_rate
        f = 441  # frequency
        length = 0.35  # s,

        N, tau = 1, 4000
        time = np.arange(sample_rate * length)

        sample = 0.9 * np.sin(2 * np.pi * f / sample_rate * time)

        decay = N * np.exp(-time/tau)
        waveform = sample * decay
        return waveform * 0.6

    @staticmethod
    def attention():
        # fs = 44100  # sampling sample_rate
        f = 341  # frequency
        length = 0.25  # s,

        time = np.arange(sample_rate * length)

        waveform = \
            1.0 * np.sin(f * np.pi * time) + \
            1.0 * np.sin(f * constants.golden * np.pi * time)

        N, tau = 1, 3000
        decay = N * np.exp(-time/tau)

        sample = waveform * decay * 0.75

        sam = np.concatenate((
            sample[::-1]*1,
            sample,
        ), axis=0)

        return sam * 0.25

    @staticmethod
    def boop():
        f = 650  # frequency
        length = 0.15  # s,
        time = np.arange(sample_rate * length)
        return 1 * np.sin(2 * np.pi * f / sample_rate * time)

    @staticmethod
    def aircraft_seatbelt():
        f = 441  # frequency
        length = 0.5  # s

        N, tau = 1, 14000

        time = np.arange(sample_rate * length)

        sample = np.sin(2 * np.pi * f / sample_rate * time)

        decay = N * np.exp(-time/tau)
        waveform = sample * decay
        '''
        samples = np.concatenate((
            audio.tone_aircraft_seatbelt(),
            np.zeros(6500),
            audio.tone_aircraft_seatbelt(),
        ), axis=0)
        '''
        return 0.6 * waveform

    @staticmethod
    def bell():

        f = 4444  # frequency
        length = 0.25  # s

        tau = 14000

        time = np.arange(sample_rate * length)

        sample = np.sin(2 * np.pi * f / sample_rate * time)

        waveform = sample * np.exp(-time / tau)
        return 0.4 * waveform




    # duration = 1  # seconds
    # fs = 44100
    # recording = sd.rec(int(duration * fs), sample_rate=fs, channels=2)

    # sd.query_devices()
    @staticmethod
    def rising():
        # calculate note frequencies
        A_freq = 440
        Csh_freq = A_freq * 2 ** (4 / 12)
        E_freq = A_freq * 2 ** (7 / 12)

        # get timesteps for each sample, T is note duration in seconds
        T = 0.25
        t = np.linspace(0, T, int(T * sample_rate), False)

        # genesample_rate sine wave notes
        A_note = np.sin(A_freq * t * 2 * np.pi)
        Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
        E_note = np.sin(E_freq * t * 2 * np.pi)

        # concatenate notes
        audio = np.hstack((A_note, Csh_note, E_note))

        return audio * 0.5



def play(sample, device=None):
    cuttoff_samples = int(sample_rate / 10)  # 0.1 seconds
    if len(sample) > cuttoff_samples: 
        time = np.arange(cuttoff_samples)
        N, tau = 1, 1600
        decay = N * np.exp(-time/tau)
        
        sample[-cuttoff_samples:] = sample[-cuttoff_samples:] * decay
        # modify end of signal
    if not device:
        return sd.play(sample, 44100)
    else:
        return sd.play(
            sample, 
            44100,
            device=device,
        )
    

'''
def notes():
    notes = 'C,C#,D,D#,E,F,F#,G,G#,A,A#,B,C'.split(',')
    freqs = 440. * 2**(np.arange(3, 3 + len(notes)) / 12.)
    notes = list(zip(notes, freqs))
    return notes
'''

'''
def notes_df():
    notes = 'C,C#,D,D#,E,F,F#,G,G#,A,A#,B,C'.split(',')
    freqs = 440. * 2**(np.arange(3, 3 + len(notes)) / 12.)
    df = pd.DataFrame(np.column_stack([
        notes, freqs/8, freqs/4, freqs/2, freqs/1, freqs*2, freqs*4
    ]))
    df = df.set_index(0).astype(float).round(2)
    return df
'''