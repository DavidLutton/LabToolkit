from ..Instrument import Instrument


class HP8903B(Instrument):
    """8903B 20 Hz to 100 kHz Audio Analyzer.

    .. figure::  images/AudioAnalyser/HP8903B.jpg
    """

    HP8903_errors = {
        10: "Reading too large for display",
        11: "Calculated value out of range",
        13: "Notch cannot tune to input",
        14: "Input level exceeds instrument specifications",
        17: "Internal voltmeter cannot make measurement",
        18: "Source cannot tune as requested",
        19: "Cannot confirm source frequency",
        20: "Entered value out of range",
        21: "Invalid key sequence",
        22: "Invalid Special Function prefix",
        23: "Invalid Special Function suffix",
        24: "Invalid HP-IB code",
        25: "Top and bottom plotter limits are identical",
        26: "RATIO not allowed in present mode",
        30: "Input overload detector tripped in range plot",
        31: "Cannot make measurement",
        32: "More than 255 points total in a sweep",
        96: "No signal sensed at input",
    }  # https://github.com/cosmonaut/hp8903/blob/master/hp8903.py

    HP8903_measurement_modes = {
        0: "THD+n",
        1: "Frequency Response",
        2: "THD+n (Ratio)",
        3: "Frequency Response (Ratio)",
        4: "Output Level",
    }  # https://github.com/cosmonaut/hp8903/blob/master/hp8903.py

    HP8903_filters = [
        "30 kHz Low Pass",
        "80 kHz Low Pass",
        "Left Plug-in Filter",
        "Right Plug-in Filter",
    ]  # https://github.com/cosmonaut/hp8903/blob/master/hp8903.py

    
'''
# Audio analyser

inst.write(f'FRQ {1e3} Hz')
inst.write(f'M1')
inst.write(f'T0')
inst.write(f'AMP {0.33} V')
inst.write(f'D0')
'''

'''
inst.write(f'FRQ {1e3} Hz')
inst.write(f'M1')
inst.write(f'T0')
inst.write(f'AMP {0.33} V')
inst.write(f'DTY {77} %')
inst.write(f'WID {77} MS')
inst.write(f'OFS {1} V')

inst.write(f'D0')

for q in [#
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


IFRQ  :   FRQ 1.00 KHZ
IDTY  :   DTY 77 %
IWID  :   WID 77.0 MS
IAMP  :   AMP 330 MV
IOFS  :   OFS +1.00 V
IHIL  :   HIL +1.16 V
ILOL  :   LOL +0.83 V
IERR  :   NO ERROR



inst.query('CST').strip().split(',')

['M1',
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
# C0  off complment output
# C1 on complment output
# D0 Disable
# D1 Enable
# L0 output limits off
# L1 output limits on

'''

freqlist = [30, 50, 100, 250, 300, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 30000]

'''
H1 left filter
H2 right filter
H0 All LR filter off
L1 30kHz LP filter
L2 80kHz LP filter
L0 all  LP filter off
R1 Ratio on
R0 Ratio off
LG Log
LN Lin

Trigger modes:
T0 Free run
T1 Hold
T2 Trigger immediate
T3 Trigger with setting

Misc

RL read left display
RR read right display
RF rapid frequency count
RS rapid source

SP SPCL
SS SPCL SPCL

FR Frequency
FA Start frequency
FB Stop frequency
PL Plot limit
FN Frequency increment
AP amplititude
AN amplititude increment

CL Clear

KZ kHz
VL V
UL upper limit
HZ Hz
MV mV
LL lower limit
DB dB
DV dBm into 600ohm

W1 Sweep on
W0 Sweep off
UP step up
DN step down

AU Automatic operation


A0 RMS detector
A1 AVG detector
AN amplitiude increment
AP Amplitude

M1 AC Level
M2 SINAD
M3 Distortion

S1 DC Level
S2 Signal-to-Noise
S3 Distortion level

Manuals/H/HP_Agilent_Keysight/8/89/8903/HP%208903B%20Operation%20&%20Calibration.pdf

Page 3-39
### Preseet settings on 3-52
M1
AP1.5VL


'''
'''

    inst.write(f'FRQ {1e3} Hz')
    inst.write(f'M1')
    inst.write(f'T0')
    inst.write(f'AMP {0.33} V')
    inst.write(f'D0')


    print(float(inst.query('RL')), float(inst.query('RR')))  # Read left, read right

print(float(inst.query('RL')), float(inst.query('RR')))  # Read left, read right
print(float(inst.query('T3')))  # Trigger with settling
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
'''
