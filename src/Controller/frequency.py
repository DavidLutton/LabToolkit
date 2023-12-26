from dataclasses import dataclass


@dataclass
class FrequencyGroupMember:
    """Class for keeping state as used in a FrequencyGroup.
    
    This allows for LO & Mixers or offsets eg -100 kHz
    """
    Instrument: None
    Ratio: float = 1
    Offset: float = 0


class FrequencyGroup():
    """Create a group of objects that share an attribute during a test and can be set together."""
    
    def __init__(self):
        self.equipment = []
    
    def add_member(self, member):
        if hasattr(member.Instrument, 'frequency'):
            self.equipment.append(member)

    @property
    def frequency(self):
        return getattr(self, 'set_frequency', 0)

    @frequency.setter
    def frequency(self, frequency):
        self.set_frequency = frequency
        for eq in self.equipment:
            eq.Instrument.frequency = self.set_frequency * eq.Ratio + eq.Offset


@dataclass
class FrequencyVoltageAdaptor():
    Instrument: None
    MinV: float = 0
    MaxV: float = 0
    MinF: float = 0
    MaxF: float = 10e9
    OffsetV: float = 0
    

    @property
    def frequency(self):
        return NotImplemented
        
    @frequency.setter
    def frequency(self, frequency):
        pass

    @property
    def voltage(self):
        return NotImplemented
        
    @voltage.setter
    def voltage(self, voltage):
        pass