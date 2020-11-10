import numpy as np

from ..GenericInstrument import GenericInstrument


class HP85nn(GenericInstrument):  # Analyser

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

    # an.query('*ID?')

    @property
    def span(self):
        """."""
        return self.query_float('SP?')

    @span.setter
    def span(self, span):
        self.write(f'SP {span} Hz')

    @property
    def sweeptime(self):
        """."""
        return self.query_float('ST?')

    @sweeptime.setter
    def sweeptime(self, sweeptime):
        if sweeptime is not -1:
            self.write(f'ST {sweeptime}s')
        else:
            self.write(f'ST AUTO')

    @property
    def reflevel(self):
        """."""
        return self.query_float('RL?')

    @reflevel.setter
    def reflevel(self, reflevel):
        self.write(f'RL {reflevel} DB')

    @property
    def resbw(self):
        """."""
        return self.query_float('RB?')

    @resbw.setter
    def resbw(self, resbw):
        self.write(f'RB {resbw} Hz')

    @property
    def frequency(self):
        """."""
        if self.span == 0.0:  # [6e9, 18e9]
            fa = self.query_float(f'FA?')
            fb = self.query_float(f'FB?')
            return [fa, fb]
        else:  # 12e9
            return self.query_float(f'CF?')

    @frequency.setter
    def frequency(self, frequency):
        if type(frequency) is list:  # [6e9, 18e9]
            self.write(f'FA{frequency[0]}Hz')
            self.write(f'FB{frequency[1]}Hz')
        else:  # 12e9
            self.write(f'CF{frequency}Hz')

    @property
    def amplitude(self):
        """."""
        self.write('MKPK HI')
        return self.query_float('MKA?')

    @property
    def trace(self):
        y = self.inst.query_ascii_values('TRA?', container=np.array)
        if self.span == 0.0:
            x = np.linspace(0, self.sweeptime, len(y))
        else:
            x = np.linspace(self.query_float('FA?'), self.query_float('FB?'), len(y))
        return x, y

        # plt.plot(*analyser.trace)
        # pd.DataFrame(np.column_stack((sa.trace)), index=None, columns=['Frequency', 'Amplitude'])
        # pd.DataFrame(np.column_stack((sa.trace)), index=None, columns=['Frequency (Hz)', 'Amplitude (dBm)']).set_index('Frequency (Hz)').plot()
