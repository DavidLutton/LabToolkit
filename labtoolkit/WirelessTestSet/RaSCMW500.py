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
        return NotImplementedError
        