from ..GenericInstrument import GenericInstrument
# from ..IEEE488 import IEEE488


class RohdeSchwarzNRVS(GenericInstrument):
    """Rohde-Schwarz NRVS.

    .. figure::  images/PowerMeter/RohdeSchwarzNRVS.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = ''

        self.write('KA0')
        self.write('KF1')  # enable freq correction
        self.write('M0')  # Average power
        self.write('N1')  # Without alphaheader

        '''
        inst.query('ZV')
        inst.query('Z2')
        inst.query('ST')
        '''

    @property
    def frequency(self):
        """."""
        return self.query_float('Z2')

    @frequency.setter
    def frequency(self, frequency):
        self.write(f'DF{int(frequency)}')

    @property
    def amplitude(self):
        """."""
        # '   DBM   6.94910E+00'
        return self.query_float('X3')

    '''
    @property
    def measurement(self):
        """Get reading of power level."""
        vals = self.query('x3').strip().split(' ')
        unit = vals[0]
        value = float(vals[-1])
        # print('{} {}'.format(value, unit))
        return(value)
    '''


'''
correctiona = {  # Correction off, TMS931, UKAS ETC D25010A, 2016/11
    0.1e6: 102.37,
    0.3e6: 100.86,
    0.5e6: 100.74,
    1e6: 100.73,
    3e6: 100.75,
    5e6: 100.78,
    10e6: 100.51,
    30e6: 100.18,
    50e6: 100.00,
    100e6: 99.95,
    300e6: 99.72,
    500e6: 99.65,
    1000e6: 99.67,
    1500e6: 100.30,
    2000e6: 101.24,
    2500e6: 102.63,
    3000e6: 104.18,
    3500e6: 105.58,
    4000e6: 107.82,
    4500e6: 107.67,
    5000e6: 105.18,
    5500e6: 100.79,
    6000e6: 96.06,
}

correctionb = {  # Correction off, TMS931, UKAS ETC E9027A, 2018/11
    0.1e6: 102.08,
    0.3e6: 100.26,
    0.5e6: 100.08,
    1e6: 100.04,
    3e6: 100.13,
    5e6: 100.18,
    10e6: 100.26,
    30e6: 100.08,
    50e6: 100.00,
    100e6: 99.93,
    300e6: 99.67,
    500e6: 99.58,
    1000e6: 99.67,
    1500e6: 100.39,
    2000e6: 101.46,
    2500e6: 102.84,
    3000e6: 104.40,
    3500e6: 105.94,
    4000e6: 108.21,
    4500e6: 108.18,
    5000e6: 105.56,
    5500e6: 101.06,
    6000e6: 96.27,
}

# TODO: Splitter balance in % or dB terms
pprint(correctiona)
keys, values = zip(*correctiona.items())
print(keys)
print(values)

fig, ax = plt.subplots()
# fig.tight_layout()
ax.set_xscale('log')
ax.plot(keys, values)
keys, values = zip(*correctionb.items())
ax.plot(keys, values)
ax.grid(True, which='both')
plt.title('TMS931 Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Correction (%)')
plt.show()
'''
