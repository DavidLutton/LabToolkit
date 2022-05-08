from ..IEEE488 import IEEE488
from ..SCPI import SCPI


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
        print(*args)
        # print(**kwargs)
        # print("Inside __call__()")
        setpoint = float(*args)
        if setpoint > f._amplitudelimit:
            print(f"Amplimit ({f._amplitudelimit}) reached with setpoint ({setpoint}) on {f.inst}")
        else:
            self.f(f, *args)
        # print("After self.f(*args)")


class HP83752B(IEEE488, SCPI):
    """."""

    def __post__(self):
        self._amplitudelimit = 0

    '''
    inst.query('ROSCillator:SOURce?'), inst.query('ROSCillator:SOURce:AUTO?')
    inst.write('ROSCillator:SOURce INTernal')
    inst.write('ROSCillator:SOURce:AUTO 1')
    '''
    @property
    def frequency(self):
        return float(self.inst.query('SOURce:FREQuency:CW?'))
    
    @frequency.setter
    def frequency(self, frequency):
        self.inst.write(f'SOURce:FREQuency:CW {frequency:.2f} Hz')
        
    @property
    def amplitude(self):
        return float(self.inst.query('SOURce:POWer:LEVel:AMPLitude?'))
    
    @amplitude.setter
    @amplitudelimiter
    def amplitude(self, power):
        self.inst.write(f'SOURce:POWer:LEVel:AMPLitude {power:.2f} DBM')
        
    @property
    def output(self):
        """."""
        if self.inst.query('OUTPut:STATe?') == '+1':
            return True
        else:
            return False

    @output.setter
    def output(self, boolean=False):
        self.inst.write(f'OUTPut:STATe {boolean:d}')