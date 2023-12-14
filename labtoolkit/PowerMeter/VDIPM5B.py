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

    def reading_formula(self, SelectedRange, countvalue):
        """Convert reading data into a reading."""
        reading = countvalue * 2. * (SelectedRange / 59576)
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
        
    def decoderD(self, data):
        """Decode a D packet of reading & state"""

        bitmap = [f'{byte:08b}' for byte in data]

        AutoRange = True if bitmap[4][7] == '1' else False

        CalibrationHeater = bitmap[4][1+3:4+3]
        CalibratiorSwitchRear = bitmap[4][1:4]
        Remote = True if bitmap[4][0] == '1' else False
        SelectedRange = bitmap[6][0:3]

        CalFactorSign = -1 if bitmap[6][3] == '1' else 1
        CalFactorTens = int(bitmap[6][4:8], 2)
        CalFactorOnes = int(bitmap[5][0:4], 2)
        CalFactorDeci = int(bitmap[5][4:8], 2)

        CalibrationFactor = CalFactorSign * (CalFactorTens * 10 + CalFactorOnes + CalFactorDeci / 10)

        match CalibrationHeater:
            case '000':
                CalibrationHeater = False
            case '001':
                CalibrationHeater = 0.1e-3
            case '010':
                CalibrationHeater = 1e-3
            case '011':
                CalibrationHeater = 10e-3
            case '100':
                CalibrationHeater = 100e-3

        match CalibratiorSwitchRear:
            case '000':
                CalibratiorSwitchRear = False
            case '001':
                CalibratiorSwitchRear = 0.1e-3
            case '010':
                CalibratiorSwitchRear = 1e-3
            case '011':
                CalibratiorSwitchRear = 10e-3
            case '100':
                CalibratiorSwitchRear = 100e-3
     
        match SelectedRange:
            case '000':
                SelectedRange = False
            case '001':
                SelectedRange = 0.2e-3
            case '010':
                SelectedRange = 2e-3
            case '011':
                SelectedRange = 20e-3
            case '100':
                SelectedRange = 200e-3
            case '111':
                SelectedRange = None
        
        watt = instd.reading_formula(SelectedRange, struct.unpack('<h', data[2:4])[0])
        # dBm = WattTo.dBm(watt).round(3) if watt > 0 else -100
        return self.Reading(
            watt, 
            AutoRange, 
            CalibrationHeater, 
            CalibratiorSwitchRear, 
            Remote, 
            CalibrationFactor, 
            SelectedRange,
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