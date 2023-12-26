import numpy as np
from dataclasses import dataclass

from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class RaSCMU200Audio(Instrument, SCPI):
    """."""
    def __post__(self):
        # if seconday
        self.write('INITiate:AFANalyzer:PRIMary')

        self.write('INITiate:AFGenerator:PRIMary')
        # print(inst.query('SOURce:AFGenerator:PRIMary:LEVel?'))
        # print(inst.query('FETCh:AFGenerator:PRIMary:STATus?'))

        # inst.write('CONFigure:AFANalyzer:PRIMary:FILTer:WEIGhting A')
        # inst.write('CONFigure:AFANalyzer:PRIMary:FILTer:WEIGhting CCI')
        # inst.write('CONFigure:AFANalyzer:PRIMary:FILTer:WEIGhting CME')
        # inst.write('CONFigure:AFANalyzer:PRIMary:FILTer:WEIGhting OFF')

        # print(self.query('CONFigure:AFANalyzer:PRIMary:FILTer:WEIGhting?'))

    @dataclass
    class AFResults:
        """Class for keeping results from Audio analyer on a CMU 200."""
        PeakVoltage1: float
        RMSVoltage1: float
        THDpN: float
        DCVoltage: float
        PeakVoltage2: float
        RMSVoltage2: float
        Frequency: float
        SINAD: float
        # THD: float MIA

    def Measurement(self):
        # print(inst.query('FETCh:AFANalyzer:PRIMary:STATus?'))
        data = self.query_ascii_values('READ:SCALar:AFANalyzer:PRIMary?', container=np.array)
        return self.AFResults(*data)
