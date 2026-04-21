from ..IEEE488 import IEEE488
from ..SCPI import SCPI
import numpy as np
import pandas as pd

import PIL.Image as Image
import io


class RigolDS1nnnZ(IEEE488, SCPI):
    '''.'''
    
    def screenshot(self):
        """."""
        data = self.query_binary_values(
            'DISPlay:DATA? 0, 0, TIFF',
            datatype='B',
            is_big_endian=False,
            container=bytearray
        )
        return Image.open(io.BytesIO(data))

    @property    
    def channels(self):
        """."""
        NUMBER_ANALOG_CHS = int(self.Model[5])
        return np.arange(1, NUMBER_ANALOG_CHS + 1)

    def displayed(self, channel):
        """."""
        return self.query_bool(f':CHANnel{channel}:DISPlay?')

    def get_traces_from_displayed_channels(self):
        """."""
        # # Actually find which channels are on, have acquired data, and get the pre-amble info if needed.
        # # The assumption here is that, if the channel is off, even if it has data behind it, data will not be retrieved from it.
        # # Note that this only has to be done once for repetitive acquisitions if the channel scales (and on/off) are not changed.

        displayed_channels = [channel for channel in self.channels if self.displayed(channel) == True]

        return displayed_channels

    def trace(self, channel):
        """."""
        self.write(f':WAVEFORM:SOURCE CHANNEL{1}')
        self.write(':WAV:FORM BYTE')
        self.write(":WAV:MODE NORM")
        #self.write(":WAV:MODE RAW")
        self.write(":WAV:MODE NORM")
        
        trace = self.query_binary_values(':WAV:DATA?', datatype='B', container=np.array)
        
        points = len(nums)
        xincr = self.query_float(':WAVeform:XINCrement?')
        xzero = self.query_float(':WAVeform:XORigin?')
       
        ydata = nums
        yoffs = 0
        ymult = self.query_float(':WAVeform:YINCrement?')
        yzero = -1
        
        x = np.arange(points) * xincr + xzero
        y = ((trace - yoffs) * ymult) + yzero
        # TODO fix / confirm offset behavour
        return pd.DataFrame(np.column_stack((x, y)), columns=['Time (s)','Channel (V)']).set_index('Time (s)')
