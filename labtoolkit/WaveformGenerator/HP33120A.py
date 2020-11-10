from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class HP33120A(IEEE488, SCPI):
    """."""

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'

        # self.amps = [0.01, 5]
        # self.freqs = [0, 15e6]

    def state(self):
        """."""
        print(f"Amplitude: {self.amplitude}")
        print(f"Frequency: {self.frequency}")
        print(f"Shape: {self.shape}")
        print(f"Load: {self.load}")
        # print("Output: {}".format(self.output))

    @property
    def frequency(self):
        """."""
        return float(self.query("SOURce:FREQuency?"))

    @frequency.setter
    def frequency(self, frequency):
        self.write(f"SOURce:FREQuency {frequency:.4f}")

    @property
    def shape(self):
        """."""
        return self.query("SOURce:FUNCtion:SHAPe?")

    @shape.setter
    def shape(self, shape="SIN"):
        # SIN|SQU|TRI|RAMP|NOIS|DC|USER
        self.write(f"SOURce:FUNCtion:SHAPe {shape}")

    @property
    def load(self):
        """."""
        return self.query("OUTPut:LOAD?")

    @load.setter
    def load(self, load="INF"):
        # 50 | INF | MAX | MIB
        self.write(f"OUTPut:LOAD {load}")

    @property
    def amplitude(self):
        """VPP|VRMS|DBM|DEF."""
        self.query("SOURce:VOLTage:UNIT?")
        return float(self.query("SOURce:VOLTage?"))
        # return(self.query("SOURce:VOLTage:UNIT?"))

    @amplitude.setter
    # @AmplitudeLimiter
    def amplitude(self, amplitude, unit="VRMS"):
        self.write(f"SOURce:VOLTage:UNIT {unit}")
        self.write(f"SOURce:VOLTage {amplitude:.6f}")

    @property
    def arb(self):
        """."""
        timeout = self.inst.timeout
        self.inst.timeout = 10000

        self.inst.timeout = timeout
        return NotImplemented

    @arb.setter
    def arb(self, waveform):
        # if len(waveform) < 16000:
        timeout = self.inst.timeout
        self.inst.timeout = 10000
        self.write_binary_values('DATA:DAC VOLATILE, ', waveform, datatype='h', is_big_endian=True)  # -2047 and +2047
        self.inst.timeout = timeout
    '''
    wavegen.write('DATA:COPY P2B, VOLATILE')
    wavegen.query('DATA:CAT?')

    wavegen.write('FREQ 2.5;VOLT 1.2')
    wavegen.write('FUNC:USER VOLATILE')
    wavegen.write('FUNC:SHAP USER')

    '''
