
from .SCPISignalGenerator import SCPISignalGenerator
# from .helper import SignalGenerator, amplitudelimiter
import numpy as np
import PIL.Image as Image
import io
from time import sleep


class AgilentE4438C(SCPISignalGenerator):
    """."""

    def arb_read(self, waveform):
        arb = self.query_binary_values(
            f':MEM:DATA? "{waveform}"',
            datatype='h',
            container=np.float64,
            is_big_endian=True
        )
        return arb.view(np.complex128)
        
    def arb_send(self, name, waveform):
        """±32384."""
        # iq.view(np.float64).astype(np.int16)
        return self.write_binary_values(
            f':MEM:DATA "WFM1:{name}",',
            waveform,
            datatype='h', 
            is_big_endian=True
        )
    
    def arb_catalog(self):
        return self.query(':MEM:CATalog? "WFM1:"')
    
    def screenshot(self):
        self.write(f':DISPlay:REMote {True:b}')
        # inst.query(':DISPlay:REMote?')

        self.write(':DISPlay:CAPTure')

        sleep(0.5)
        self.query_bool('*OPC?')
        bins = self.query_binary_values(
            ':MEM:DATA? "BINARY:DISPLAY.BMP"', 
            datatype='B',
            is_big_endian=False,
            container=bytearray
        )
        # image.save('FILENAME.png')
        return Image.open(io.BytesIO(bins))
        