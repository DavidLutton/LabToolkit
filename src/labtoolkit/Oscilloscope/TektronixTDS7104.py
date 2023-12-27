# TEKTRONIX,TDS7104,B031652,CF:91.1CT FV:2.2.0

from ..IEEE488 import IEEE488
from ..SCPI import SCPI

from time import sleep
from datetime import datetime as dt

import PIL.Image as Image
import io


class TektronixTDS7104(IEEE488,):
    """."""

    def __post__(self):
        now = dt.now()
        
        self.write(f'DATE "{now.year}-{now.month}-{now.day}"')
        self.write(f'TIME "{now.hour}:{now.minute}:{now.second}"')

    def screenshot(self):
        """."""
        self.write('HARDCOPY:FILENAME "C:/FILE.BMP"')
        # self.write('HARDCopy:PORT Gpib') # Printer
        self.write('HARDCopy:IMAGe NORMal')
        self.write('HARDCopy:PALEtte COLOr')
        self.write('HARDCopy:VIEW FULLSCREEN') # GRAticule

        self.write('HARDCopy STArt')
        sleep(1)
        self.write('FILESYSTEM:READFILE "C:/FILE.BMP"')
      
        img = Image.open(io.BytesIO(self.inst.read_bytes(921654)))
        self.write('FILESYSTEM:DELETE "C:/FILE.BMP"')
        return img



'''



inst.write('DATA:SOURCE CH3')

# inst.write('DATA:ENCDG RIBINARY;WIDTH 1')
inst.write('DATA:ENCDG ASCIi;WIDTH 1')
inst.write('HORIZONTAL:RECORDLENGTH 500')
inst.write('DATA:START 1')
inst.write('DATA:STOP 500')
inst.write('HEADER OFF')

inst.write('ACQUIRE:STATE RUN')  # Make sure setup changes have taken effect and a new waveform is acquired

# * Read the waveform preamble.
# inst.query('WFMPRE:CH3:NR_PT?;YOFF?;YMULT?;XINCR?;PT_OFF?;XUNIT?;YUNIT?')
# inst.query('WFMOutpre?')
# inst.query('WFMPRE:CH3:NR_PT?;YOFF?;YMULT?;XINCR?;PT_OFF?;XUNIT?;YUNIT?')
#  * Output header (x-, y-units, date, time and source)
SampleInterval = float(inst.query('WFMOUTPRE:XINCR?'))
yunit = inst.query('WFMOUTPRE:YUNIT?')
ymult = float(inst.query('WFMOUTPRE:YMULT?'))
yoff = float(inst.query('WFMOUTPRE:YOFF?'))
yzero = float(inst.query('WFMOUTPRE:YZERO?'))
# waveform_raw = inst.query_binary_values('CURVE?', container=np.float32)
waveform_raw = inst.query_ascii_values('CURVe?', container=np.int8)

y = ymult * (waveform_raw - yoff) - yzero  #  Now that we have the data we can convert the numbers into voltages
x = np.arange(0, 500) * SampleInterval


plt.figure(figsize=[6.4*5, 4.8*3])

# plt.xscale('log')
plt.grid(which='both')
# plt.title('Combined')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('dB')
plt.plot(x, y, label='foo')
plt.plot(x, y2, label='foo')
plt.plot(x, y3, label='foo')


# plt.plot(waveform_raw)
plt.legend(loc='lower left', fontsize='x-large')


inst.write('DATA:SOURCE CH3')
inst.query(':HORIZONTAL:RECORDLENGTH?')
'''