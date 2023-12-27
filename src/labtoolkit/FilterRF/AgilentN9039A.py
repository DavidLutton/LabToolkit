from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class AgilentN9039A(IEEE488, SCPI):
    """."""

    def status(self):
        """."""
        return {
            'Gain': self.gain,
            'Attenuation': self.attenuation,
            'Feed': self.feed,
            'Path': self.path,
            'FilterBank': self.filterbank,
            'Conducted': self.conducted,
            'Radiated': self.radiated,
            'Center': self.center,
            'Center (MHz)': self.center / 1e6,
        }

    def states(self):
        """."""
        return {
            'Gain': [0, 1],
            'Attenuation': [10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5],
            # list(np.linspace(10, 57.5, 20)),  # 10 to 57.5 in 20 steps
            'Feed': ['RF', 'SOUR'],
            'Path': ['BYP', 'FILT'],
            'FilterBank': ['RAD', 'COND', 'OFF'],
            'Conducted': ['COND0', 'COND1', 'COND2', 'COND3', 'COND4', 'COND5', 'COND6', 'COND7', 'COND8', 'COND9', 'COND10', 'COND11'],
            'Radiated': ['RAD0', 'RAD1', 'RAD2', 'RAD3', 'RAD4', 'RAD5', 'RAD6', 'RAD7', 'RAD8'],
        }

    @property
    def gain(self):
        """."""
        return self.query_bool(':SERV:POW:GAIN?')

    @gain.setter
    def gain(self, gain):  # True, False 0, 1
        # inst.write(':SERV:POW:GAIN 0')
        # inst.write(':SERV:POW:GAIN 1')
        return self.write(f':SERV:POW:GAIN {gain}')

    @property
    def attenuation(self):
        """."""
        return self.query_float(':SERV:POW:ATT?')

    @attenuation.setter
    def attenuation(self, attenuation):
        return self.write(f':SERV:POW:ATT {attenuation}')

    @property
    def feed(self):
        """."""
        return self.query(':SERV:FEED?')

    @feed.setter
    def feed(self, feed):
        # inst.write(':SERV:FEED SOUR')
        # inst.write(':SERV:FEED RF')
        return self.write(f':SERV:FEED {feed}')

    @property
    def path(self):
        """."""
        return self.query(':SERV:FEED:PATH?')

    @path.setter
    def path(self, path):  # BYP, FILT
        # inst.write(':SERV:FEED:PATH BYP')
        # inst.write(':SERV:FEED:PATH FILT')
        return self.write(f':SERV:FEED:PATH {path}')

    @property
    def filterbank(self):
        """."""
        return self.query(':SERV:PROD:PATH?')

    @filterbank.setter
    def filterbank(self, path):  # COND, RAD, OFF
        # inst.write(':SERV:PROD:PATH COND')
        # inst.write(':SERV:PROD:PATH RAD')
        # inst.write(':SERV:PROD:PATH OFF')
        # through paths via the filter boards 9kHz to 2MHz, 2MHz to 30MHz and 28MHz to 1GHz
        return self.write(f':SERV:PROD:PATH {path}')

    @property
    def conducted(self):
        """."""
        return self.query(':SERV:PROD:FILT:COND:BAND?')

    @conducted.setter
    def conducted(self, index):  # COND0 to COND11
        return self.write(f':SERV:PROD:FILT:COND:BAND {index}')

    @property
    def radiated(self):
        """."""
        return self.query(':SERV:PROD:FILT:RAD:BAND?')

    @radiated.setter
    def radiated(self, index):  # RAD0 to RAD8
        return self.write(f':SERV:PROD:FILT:RAD:BAND {index}')

    @property
    def center(self):
        """."""
        return self.query_float(':SERV:FREQ:CENT?')

    @center.setter
    def center(self, frequency):
        return self.write(f':SERV:FREQ:CENT {frequency}')


'''
print(inst.query('*IDN?'))
# print(inst.query('*OPT?'))


inst.write('*CLS')

inst.query(':SYST:HID?'), inst.query(':SERV:EXT:VERS?')

inst.query(':STAT:QUES:CAL:EXT:NEED:COND?')
14

inst.query(':CAL:TIME:LRAD?'), inst.query(':CAL:TIME:LCON?')  # last rad / con alignment


# inst.query(':SERV:CAL:DATA? 100905')

# inst.query(':SERV:CAL:DATA? 100907')



'''
'''
flt = AgilentN9039A(inst)

flt.gain, flt.attenuation, flt.feed, flt.path, flt.filterbank, flt.conducted, flt.radiated, flt.center
('0', 10.0, 'RF', 'BYP', 'OFF', 'COND0', 'RAD0', 13249999999.0)


# flt.path = 'FILT'
# flt.filterbank = 'COND'
# flt.conducted = 'COND5'
# flt.feed = 'SOUR'

# flt.attenuation = 10
# flt.center =
if inst.query(':SERVice:HARD:SETT;*OPC?') == '1':
    print('Carry on')

# inst.query(':SERV:PROD:FILT:THROUGH?')
flt.gain = 0
inst.query('SYST:ERR?')
inst.write('*RST')
flt.status()

for k, v in flt.states().items():
    print(f'{k} : {v}')

flt.states()['Radiated']

flt.path, flt.filterbank, flt.radiated = 'FILT', 'RAD', 'RAD3'

flt.center = 750e6
flt.center
flt.path, flt.filterbank, flt.conducted = 'FILT', 'COND', 'COND11'
'''


'''
Internal spurious on 3 units of Agilent N9039A

651.5e6 CF
peak as ~-3 dBuV
50kHz side tones  ~ -13 dBuV
1e6 span
~ -20 dBuV floor
1kHz BW
100 AV
atten 0dB
gain on
'''
