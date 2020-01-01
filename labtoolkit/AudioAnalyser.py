#!/usr/bin/env python3
"""."""

import time
import logging
# import pint

from labtoolkit.GenericInstrument import GenericInstrument
from labtoolkit.IEEE488 import IEEE488
from labtoolkit.SCPI import SCPI


class AudioAnalyser(GenericInstrument):
    """Parent class for AudioAnalyser."""

    def __init__(self, instrument):
        """."""
        super().__init__(instrument)


class HP8903B(AudioAnalyser):
    """8903B 20 Hz to 100 kHz Audio Analyzer.

    .. figure::  images/AudioAnalyser/HP8903B.jpg
    """

    '''
    inst.write(f'FR {1e3} Hz')
    inst.write(f'M1')
    inst.write(f'T0')
    inst.write(f'AMP {0.33} V')
    inst.write(f'D0')
    "print(float(inst.query('RL')), float(inst.query('RR')))  # Read left, read right\n",
        "print(float(inst.query('T3')))  # Trigger with settling\n",

%%time
result = {}
inst.write(f'AP{5.08}VL'+f'L{0}')
#for f in np.linspace(20, 100e3, 5000):
for f in np.linspace(0.5e3, 100e3, 200):
    # for f in np.linspace(0.5e3, 1e3, 2):
    result[f] = float(inst.query(f'FR{f}HZ'+f'T{3}'+'RR'))  # Trigger with settling
    # print(f'{f}: {result[f]}')
result0 = result

inst.write('H0') # 1, 2 l,r
inst.write('L0') # 1, 2 l,r
inst.write('M1') # AC
# inst.write('M2') # Sinad
# inst.write('M3') # Distortion
# inst.write('LG')  # Log amplitude
inst.write('LN')  # Lin amplitude
inst.write('R1')  # Ratio on
inst.write('R0')  # Ratio off
inst.write('T3')  # Trigger with settling
inst.write('T0')  # Free run


            "inst.write(f'FRQ {1e3} Hz')\n",
            "inst.write(f'M1')\n",
            "inst.write(f'T0')\n",
            "inst.write(f'AMP {0.33} V')\n",
            "inst.write(f'DTY {77} %')\n",
            "inst.write(f'WID {77} MS')\n",
            "inst.write(f'OFS {1} V')\n",
            "\n",
            "inst.write(f'D0')"
p = figure(title='Frequency Response', x_axis_label='Frequency (Hz)', y_axis_label='Amplitude (V)',width=1440)  #, sizing_mode='scale_width')  # width=1800, height=900)

p.line(np.array(list(result30.keys())), np.array(list(result30.values())), legend='30kHz LP', color='black', alpha=1, line_width=2)
p.line(np.array(list(result80.keys())), np.array(list(result80.values())), legend='80kHz LP', color='blue', alpha=1, line_width=2)
p.line(np.array(list(result0.keys())), np.array(list(result0.values())), legend='No Filter', color='red', alpha=1, line_width=2)

p.legend.location = "bottom_left"
p.legend.click_policy="hide"
p.legend.background_fill_color = "black"
p.legend.background_fill_alpha = 0.25

p.ygrid.minor_grid_line_color = 'black'
p.ygrid.minor_grid_line_alpha = 0.1

p.xgrid.minor_grid_line_color = 'black'
p.xgrid.minor_grid_line_alpha = 0.1
# p.background_fill_color = "gray"

# p.background_fill_alpha = 0.2

show(p)


      "IFRQ  :   FRQ 1.00 KHZ\n",
      "IDTY  :   DTY 77 %\n",
      "IWID  :   WID 77.0 MS\n",
      "IAMP  :   AMP 330 MV\n",
      "IOFS  :   OFS +1.00 V\n",
      "IHIL  :   HIL +1.16 V\n",
      "ILOL  :   LOL +0.83 V\n",
      "IERR  :   NO ERROR \n"
    "for q in [#\n",
    "    'IFRQ',\n",
    "    'IDTY',\n",
    "    'IWID',\n",
    "    'IAMP',\n",
    "    'IOFS',\n",
    "    'IHIL',\n",
    "    'ILOL',\n",
    "    'IERR'\n",
    "    \n",
    "]:\n",
    "    print(f'{q}  :  {inst.query(q)}')\n"

    "# https://literature.cdn.keysight.com/litweb/pdf/08116-90003.pdf?id=615544 # p ~60"

HP8903_errors = {10: "Reading too large for display.",
                 11: "Calculated value out of range.",
                 13: "Notch cannot tune to input.",
                 14: "Input level exceeds instrument specifications.",
                 17: "Internal voltmeter cannot make measurement.",
                 18: "Source cannot tune as requested.",
                 19: "Cannot confirm source frequency.",
                 20: "Entered value out of range.",
                 21: "Invalid key sequence",
                 22: "Invalid Special Function prefix.",
                 23: "Invalid Special Function suffix.",
                 24: "Invalid HP-IB code.",
                 25: "Top and bottom plotter limits are identical.",
                 26: "RATIO not allowed in present mode.",
                 30: "Input overload detector tripped in range plot.",
                 31: "Cannot make measurement.",
                 32: "More than 255 points total in a sweep.",
                 96: "No signal sensed at input."}
meas_dict = {0: "THD+n",
                     1:"Frequency Response",
                     2: "THD+n (Ratio)",
                     3: "Frequency Response (Ratio)",
4: "Ouput Level"}

HP8903_filters = ["30 kHz Low Pass",
                  "80 kHz Low Pass",
                  "Left Plug-in Filter",
                  "Right Plug-in Filter"]
#             decs = math.log10(stopf/strtf)
# npoints = int(decs*num_steps)
# https://github.com/cosmonaut/hp8903/blob/master/hp8903.py


    '''
    # inst = rm.open_resource('GPIB1::4::INSTR', read_termination='\r\n')  # , write_termination='')
    inst.write(f'FRQ {1e3} Hz')
    inst.write(f'M1')
    inst.write(f'T0')
    inst.write(f'AMP {0.33} V')
    inst.write(f'DTY {77} %')
    inst.write(f'WID {77} MS')
    inst.write(f'OFS {1} V')

    inst.write(f'D0')
    for q in [
        'IFRQ',
        'IDTY',
        'IWID',
        'IAMP',
        'IOFS',
        'IHIL',
        'ILOL',
        'IERR'
    ]:
        print(f'{q}  :  {inst.query(q)}')
    '''
    IFRQ  :   FRQ 1.00 KHZ
    IDTY  :   DTY 77 %
    IWID  :   WID 77.0 MS
    IAMP  :   AMP 330 MV
    IOFS  :   OFS +1.00 V
    IHIL  :   HIL +1.16 V
    ILOL  :   LOL +0.83 V
    IERR  :   NO ERROR
    '''
    inst.query('CST').strip().split(',')
    '''
    'M1',
    'CT0',
    'T0',
    'W1',
    'H1',
    'A0',
    'L0',
    'C0',
    'D0',
    'BUR 0001 #',
    'RPT 100 MS',
    'STA 1.00 KHZ',
    'STP 100 KHZ',
    'SWT 50.0 MS',
    'MRK 1.00 KHZ',
    'FRQ 1.00 KHZ',
    'DTY 12 %',
    'AMP 330 MV',
    'OFS +000 MV',
    'WID 100 US',
    '']
    '''
    _trigger_modes = {
        'M1': 'NORM',
        'M2': 'TRIG',
        'M3': 'GATE',
        'M4': 'EWID',
    }
    _trigger_states = {
        'T0': 'Off',
        'T1': 'Positive slope',
        'T2': 'Negative slope',

    }
    _control_modes = {
        'CT0': '',
        '': '',
        '': '',
        '': '',
        '': '',
        '': '',
    }
    _Waveform = {
        'W0': 'DC',
        'W1': 'Sine',
        'W2': 'Triangle',
        'W3': 'Square',
        'W4': 'Pulse',
        '': '',
    }
    _Phase = {
        'H0': '0',
        'H1': '-90',
    }
    # C0 off complment output
    # C1 on complment output
    # D0 Disable
    # D1 Enable
    # L0 output limits off
    # L1 output limits on


REGISTER = {
    'HEWLETT-PACKARD,8903B': HP8903B,
}
