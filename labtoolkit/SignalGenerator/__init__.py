# print(f'Invoking __init__.py for {__name__}')

# from .SCPISignalGenerator import SCPISignalGenerator
from .AgilentE4422B import AgilentE4422B
from .AgilentN5181A import AgilentN5181A
from .AgilentN5182A import AgilentN5182A
from .AnritsuMG369NX import AnritsuMG369NX
from .AnritsuMG3710A import AnritsuMG3710A
from .HP866nX import HP866nX
from .HP8657A import HP8657A
from .HP83752B import HP83752B
from .HP85645A import HP85645A
from .HPESG3000A import HPESG3000A
from .IFR341n import IFR341n
from .KeysightN5173B import KeysightN5173B
from .MarconiInstruments203N import MarconiInstruments203N
from .RohdeSchwarzSHM52 import RohdeSchwarzSHM52
from .Wiltron360SS69 import Wiltron360SS69
from .Wiltron6669A import Wiltron6669A
from .Wiltron6672B import Wiltron6672B

REGISTER = {
    'Hewlett-Packard,ESG-4000B': AgilentE4422B,
    'Agilent Technologies,E4422B': AgilentE4422B,  # Real?

    'MARCONI INSTRUMENTS,2030': MarconiInstruments203N,
    'MARCONI INSTRUMENTS,2031': MarconiInstruments203N,
    'MARCONI INSTRUMENTS,2032': MarconiInstruments203N,

    'ANRITSU,MG3691A': AnritsuMG369NX,
    'ANRITSU,MG3691B': AnritsuMG369NX,
    'ANRITSU,MG3692A': AnritsuMG369NX,
    'ANRITSU,MG3692B': AnritsuMG369NX,
    'ANRITSU,MG3693A': AnritsuMG369NX,
    'ANRITSU,MG3693B': AnritsuMG369NX,
    'ANRITSU,MG3694A': AnritsuMG369NX,
    'ANRITSU,MG3694B': AnritsuMG369NX,
    'ANRITSU,MG3695A': AnritsuMG369NX,
    'ANRITSU,MG3695B': AnritsuMG369NX,

    'HEWLETT-PACKARD,8657A': HP8657A,

    'HEWLETT-PACKARD,83752B': HP83752B,

    'HEWLETT_PACKARD,8664A': HP866nX,
    'HEWLETT_PACKARD,8665B': HP866nX,
    'Wiltron,6669A,NO_IDN': Wiltron6669A,  # TODO
    'Wiltron,6672B,NO_IDN': Wiltron6672B,  # TODO
    'Wiltron,360SS69,NO_IDN': Wiltron360SS69,  # TODO
    'ANRITSU,MG3710A': AnritsuMG3710A,
    'Keysight,N5173B': KeysightN5173B,
    'ROHDE&SCHWARZ,SMH52': RohdeSchwarzSHM52,
    'HEWLETT-PACKARD,85645A': HP85645A,
    'Agilent Technologies,N5181A': AgilentN5181A,
    'Agilent Technologies,N5182A': AgilentN5182A,
    # 'TBC, IFR, 341n': IFR341n, 
    'TBC, E131': HPESG3000A,
    # HP 8673M 2-18GHz
    # Anritsu MG3710A 100e3, 6e9
    # Agilent N5182A 100e3, 6e9
    # Benchview supported E4438C, E4428C, E8267D, E8257D, E8663D, N5171B,N5172B, N5173B, N5181A/B, N5182A/B, N5183A/B
}
