class FrequencyCounter():
    """."""

    def frequency(self):
        return NotImplemented

    def frequency_error(self, target=10e6):
        """."""
        return round(self.frequency - target, 8)
