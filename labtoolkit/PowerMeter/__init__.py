# print(f'Invoking __init__.py for {__name__}')

from .AgilentE4418B import AgilentE4418B
from .HP437B import HP437B
from .RohdeSchwarzNRVS import RohdeSchwarzNRVS

REGISTER = {
    'HEWLETT-PACKARD,E4418B': AgilentE4418B,
    'Agilent Technologies,E4418B': AgilentE4418B,
    'Rohde&Schwarz,NVRS,NO_IDN': RohdeSchwarzNRVS,
    'HEWLETT-PACKARD,437B,': HP437B,
}

'''
REGISTER = {
    # R&S ???4
    # Bird 4421
    # Benchview Supported N1911A, N1912A, N1913A, N1914A, N8262A,
    # Benchview Supported U2000A, U2000B, U2000H, U2001A, U2001B, U2001H, U2002A, U2002H, U2004A, U2021XA, U2022XA, U2041XA, U2042XA, U2043XA, U2044XA, U2049XA LAN, U8481A, U8485A, U8487A, U8488A
}
'''
