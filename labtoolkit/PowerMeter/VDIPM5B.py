from ..Instrument import Instrument
from time import sleep
from dataclasses import dataclass


class VDIPM5B(Instrument):
    """VDI PM5B"""

    def __post__(self):
        self.inst.query_delay = 0.05
        
    def padding(self, cmd):
        """Format command string by adding padding & termination."""
        nulls = b'\x00'
        end = b'\x0d'
        pads = 7 - len(cmd) 
        command = cmd.encode() + nulls * pads + end
        return command

    def reading_formula(self, rangevalue, countvalue):
        """Convert reading data into a reading."""
        match rangevalue:
            case 1:
                rangemax = 200e-6
            case 2:
                rangemax = 2e-3
            case 3:
                rangemax = 20e-3
            case 4:
                rangemax = 200e-3
        reading = countvalue * 2. * rangemax / 59576
        # where rangemax = 200.E-6 for rangeval=1, or 2.E-3 for rangeval=2, or 20.E-3 for rangeval=3, or 200.E-3 for rangeval=4. 
        # The range value setting is also available in the status bytes (see below). 
        # If there is a cal factor on the front panel, the reading from the formula above should be further modified as:
        # reading = reading * 10^(calfactor/10.)
        return reading

            
    @dataclass
    class Reading:
        """Class for holding a reading from a PM5B."""
        Watt: float
        AutoRange: bool
        CalibrationHeater: float
        CalibratiorSwitchRear: float
        Remote: bool
        CalibrationFactor: float
        SelectedRange: float
        # ReadingdBm: float
        
    def decoderD(self, bins):
        """Decode a D packet of reading & state"""
        bits = np.unpackbits(np.array([r for r in bins], dtype=np.uint8))
        
        tens, ones, decimal = bins[6] & 0x0F, bins[5] >> 4, bins[5] & 0x0F  
        CalibrationFactor = tens * 10 + ones + decimal / 10   # needs sign bit
        
        countbits = bits[8:24]
        countvalue = int(''.join([str(x) for x in countbits]), 2)
        rangevalue = 2

        AutoRange = None
        CalibrationHeater = None
        CalibratiorSwitchRear = None
        Remote = None  # what is remote
        SelectedRange = None
        
        watt = self.reading_formula(rangevalue, countvalue)
        return self.Reading(
            watt, 
            AutoRange, 
            CalibrationHeater, 
            CalibratiorSwitchRear, 
            Remote, 
            CalibrationFactor, 
            SelectedRange,
            # WattTo.dBm(watt).round(3) if watt > 0 else -100
        )
        
    def decoderVC(self, bins):
        """Decode a VC packet of firmware versions"""
        # VC....
        # Byte 3 is the decimal portion of the firmware code revision
        # Byte 4 is the integer portion of the firmware code revision
        # Byte 5 is the decimal portion of the secondary firmware code revision
        # Byte 6 is the integer portion of the secondary firmware code revision
        return NotImplemented

    def query(self, cmd):
        """Run a query."""
        self.inst.write_raw(self.padding(cmd))
        sleep(self.inst.query_delay)
        match cmd:
            case '?D1':
                he = self.inst.read_bytes(7)
                if he[0] == 6:
                    pass
                    return self.decoderD(he)
            case '?VC':
                he = self.inst.read_bytes(7)
            case _:
                he = self.inst.read_bytes(1)
        # print(he.hex())
        return he 