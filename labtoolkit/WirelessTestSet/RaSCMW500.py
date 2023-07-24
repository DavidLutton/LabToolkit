from ..IEEE488 import IEEE488
from ..SCPI import SCPI

import numpy as np
from datetime import datetime as dt

import PIL.Image as Image
import io


class RaSCMW500(IEEE488, SCPI):

    def __post__(self):
        # self.write(f':SYST:DATE "{now:%Y},{now:%m},{now:%d}"')
        # self.write(f':SYST:TIME "{now:%H},{now:%M},{now:%S}"')
        self.local
    
    def screenshot(self):
        """Capture a screenshot."""
        # Usage
        # counter = 0
        
        # image = screenshot(inst)
        # counter += 1
        # image.save(p / f'image{counter:04.0f}.png')
        
        image = Image.open(io.BytesIO(
            self.query_binary_values(
                'HCOPy:DATA?',
                datatype='B', 
                is_big_endian=False, 
                container=bytearray
            )
        ))
        self.local
        return image
        