# from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI

'''
opts = inst.query('OO').split(',')  # Anritsu output options

fmin, fmax = 2e9, 10e9
amin, amax = -30, 21

if '5' in opts:
    fmin = 10e6
if '2A' in opts:
    amin = -110
print(amin, amax, fmin, fmax)

testvalue = 24.01
if amin <= testvalue <= amax:
    print(True)
'''


class amplitudelimiter(object):
    """Class to limit upper amplitude value applied to a SignalGenerator.

    Applied by decorator @amplitudelimiter
    """

    def __init__(self, f, *args, **kwargs):
        """If there are no decorator arguments, the function to be decorated is passed to the constructor."""
        # print(f)
        # print(*args)
        # print(**kwargs)
        # print("Inside __init__()")
        self.f = f

    def __call__(self, f, *args, **kwargs):
        """The __call__ method is not called until the decorated function is called."""
        # print(f)
        # print(*args)
        # print(**kwargs)
        # print("Inside __call__()")
        setpoint = float(*args)
        if setpoint > f._amplitudelimit:
            print(f"Amplimit ({f._amplitudelimit}) reached with setpoint ({setpoint}) on {f.inst}")
        else:
            self.f(f, *args)
        # print("After self.f(*args)")


class AnritsuMG369nAB(IEEE488):
    """."""

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\r\n'
        self.inst.write_termination = '\n'
        self._fmin, self._fmax = float(self.query('OFL')) * 1e6, float(self.query('OFH')) * 1e6  # Min, Max Frequency
        self._options = [str(i) for i in self.query('OO').split(',')]  # Options installed
        self._preset_()
        self._amplitudelimit = 0

    def _preset_(self):
        self.write('CF0')  # select F0
        self.write('L0')  # select L0

        self.write('LOG')  # operate in dBm  / LIN in mV
        self.output = False
        self.write('RO1')  # RF state at reset to off

        self.frequencymultiplier = 1
        self.leveloffset = 0
        self.write('LO0')  # Level offset off

        self.write('RL')

    @property
    def frequency(self):  # Responce is in MHz
        return round(float(self.query('OF0')) * 1e6, 2)

    @frequency.setter
    def frequency(self, frequency):
        self.write(f'F0{frequency:.2f}HZ')

    @property
    def frequencymultiplier(self):
        return float(self.query('OFM'))  # Output Frequency Multiplier

    @frequencymultiplier.setter
    def frequencymultiplier(self, multiplier=1):
        self.write(f"FRS{multiplier}TMS")  # Set Frequency Multiplier

    @property
    def amplitude(self):
        return float(self.query('OL0'))  # Output Level 0

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f'L0{amplitude:.2f}DM')

    @property
    def output(self):
        return NotImplemented

    @output.setter
    def output(self, boolean=False):
        self.write(f'RF{boolean:d}')

    @property
    def leveloffset(self):
        return float(self.query('OLO'))

    @leveloffset.setter
    def leveloffset(self, leveloffset):
        self.write(f'LOS{leveloffset:.2f}DB')

    '''
    # 'F5 100 MZ ACW'  # Activate CW on open frequency param

    # AT0  # deselect coupling of ALC attenuator
    # AT1  # select coupling of ALC attenuator
    # ATT00 to ATT11 nn * 10 dB.

    # CS0  # Turns off CW Ramp

    # LVP  # set output -1dB of Peak power shy of

    # gen.query('OI')
    # gen.query('OVN')  # ROM Version

    # PS0  # Phase Offset Off
    # PSO{phase}DG

    # PU{n}
    # 0 dBm
    # 1 mV
    # 2 dBmV

    # TR0 , TR1  # when step attenuator is installed use 0 or 40dB of attenuation ~source match termination

        # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    LOS Opens the level offset
    parameter.
    +100dB to 100dB
    (logarithmic); +xxx mV to
    xxx mV (linear)
    DB (log)
    VT (linear
    # XL0
    Opens the L0 parameter.   Power level range of the
    MG369XB model
    DM (log)
    VT (linear)

    '''


'''
class AnritsuMG369nx(SignalGenerator, IEEE488):
    """ANRITSU,MG369nx."""



    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')
        # self.options = self.query("*OPT?").strip().split(',')

        # self.amps = [-110, 30]
        self.freqs = [2e9, 10e9]
        # self.write("*CLS")  # clear error status
        # self.write("*CLS")  # clear error status
        # self.write('CF0')  # Set CW mode at F0, Opens F0 parameter.
        # self.write('CM0')  # Set CW mode at M0, Opens M0 parameter.
        # AL0
        # self.write('LOG')
        # self.query('SAF')  # Outputs the current instrument setup to the controller.
        # RCF Readies the MG369XB to receive a new instrument setup recalled from the controller
        self.query('OO')  # Returns the instrument option string to the controller
        self.write('RO1')  # Selects RF to be off at reset
        self.write('RL1')  # Release to Local

    @property
    def frequency(self):
        """."""
        return(float(self.query("OF0").strip()) * 1e6)  # Responce is in MHz

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"F0{frequency:.0f} HZ")

    @property
    def amplitude(self):
        """."""
        return(self.query("OL0"))  # OLO

    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, amplitude):
        self.write(f"L0{amplitude:.2f}DM")

    @property
    def output(self):
        """."""
        return NotImplemented

        #ORF

    @output.setter
    def output(self, boolean=False):
        self.write(f"RF{boolean:d}")


class AnritsuMG3691B(AnritsuMG369nx):  # ANRITSU,MG3691B,
    """Antitsu MG3691B 2e9, 10e9.

    .. figure::  images/SignalGenerator/AnritsuMG3691B.jpg
    """

    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        assert self.IDN.startswith('ANRITSU,MG3691B,')

        self.amps = [-110, 30]
        self.freqs = [10e6, 10e9]


class AnritsuMG3692A(AnritsuMG369nx):  # ANRITSU,MG3692A,
    """Antitsu MG3692A 2e9, 20e9.

    .. figure::  images/SignalGenerator/AnritsuMG3692A.jpg
    """

    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        assert self.IDN.startswith('ANRITSU,MG3692A,')

        self.amps = [-110, 30]
        self.freqs = [10e6, 20e9]


class AnritsuMG3693A(AnritsuMG369nx):  # ANRITSU,MG3693A,
    """Antitsu MG3693A 2e9, 30e9.

    .. figure::  images/SignalGenerator/AnritsuMG3693A.jpg
    """

    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        assert self.IDN.startswith('ANRITSU,MG3693A,')

        self.amps = [-110, 30]
        self.freqs = [2e9, 30e9]


class AnritsuMG3695B(AnritsuMG369nx):  # ANRITSU,MG3695B,
    """Antitsu MG3695A 2e9, 50e9.

    .. figure::  images/SignalGenerator/AnritsuMG3695A.jpg
    """

    # Need to preset : amp offset, freq offset, used freq, used amp, used mod, used pulse

    def __repr__(self):
        """."""
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)
        # self.log.info('Creating an instance of\t' + str(__class__))
        self.log.info(f'Creating {str(__class__.__name__)} for {self.instrument}')

        # assert self.IDN.startswith('ANRITSU,MG3693A,')

        self.amps = [-110, 20]
        self.freqs = [8e6, 50e9]

'''
