

class FrequencyGroup():
    """Create a group of objects that share an attribute during a test and can be set together."""
    # Need to create one that allows for LO & Mixers
    
    def __init__(self, objects):
        
        self.objectswithfrequency = [obj for obj in objects if hasattr(obj, 'frequency')]  
        # if obj hasattr frequency, add to list
        # print(self.objectswithfrequency)
    
    @property
    def frequency(self):
        return NotImplemented 
    
    @frequency.setter
    def frequency(self, frequency):
        # print(f'Setting {self.objectswithfrequency} to {frequency} Hz')
        for obj in self.objectswithfrequency:
            obj.frequency = frequency      