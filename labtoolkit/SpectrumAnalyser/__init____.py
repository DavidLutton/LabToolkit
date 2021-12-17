from enum import IntFlag
from enum import auto as enum_auto



class Detector(IntFlag):
    QuasiPeak = enum_auto()
    Average = enum_auto()
    Peak = enum_auto()
    RMS = enum_auto()
    NegPeak = enum_auto()



from pyvisa.constants import VI_GPIB_REN_ADDRESS_GTL
