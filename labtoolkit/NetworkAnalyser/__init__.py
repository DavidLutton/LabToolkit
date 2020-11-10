# print(f'Invoking __init__.py for {__name__}')

from .maths import complexto

from .HP4395A import HP4395A
from .AgilentE8357A import AgilentE8357A
from .Wiltron360 import Wiltron360
# import .Wiltron360

REGISTER = {
    'HEWLETT-PACKARD,4395A': HP4395A,
    'Agilent Technologies,E8357A': AgilentE8357A,
    'Wiltron,360,NO_IDN': Wiltron360,

}


'''
    "Keysight, Fieldfox": KeysightFieldFox,

    # Benchview suppored:
    # ENA:  E5080A, E5061B, E5063A, E5071C, E5072A
    # PNA:  N5221A, N5222A, N5224A, N5245A, N5227A
    # PNA-L:  N5230C, N5231A, N5232A, N5234A, N5235A, N5239A
    # PNA-X:  N5241A, N5242A, N5244A, N5245A, N5247A, N5249A
    # Fieldfox: N9912A, N9913A, N9914A, N9915A, N9916A, N9917A, N9918A, N9923A, N9925A,
    #  N9926A, N9927A, N9928A, N9935A, N9936A, N9937A, N9938A, N9950A, N9951A, N9952A, N9960A, N9961A, N9962A
'''
