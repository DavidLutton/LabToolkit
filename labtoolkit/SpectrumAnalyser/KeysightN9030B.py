from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI


class KeysightN9030B(IEEE488, SCPI):
    """."""
    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        
    '''
    print(inst.query('*IDN?'))
print(inst.query('*OPT?').split(','))

Keysight Technologies,N9030B,MY56320666,A.20.25
['"550', 'B25', 'DP2', 'EP1', 'EXM', 'FS1', 'FS2', 'FSA', 'LFE', 'NF2', 'NUL', 'PFR', 'RTL', 'SSD', 'PC6', 'W7X', 'MTU"']

for q in [
    '*IDN?',
    # '*CAL?',
    ':FORM?', 
    ':INST:SEL?', 
    # ':SENS:FREQ:STAR?', 
    # ':SENS:FREQ:STOP?', 
    ':SENS:BWID:RES?',
    ':SENS:BWID:VID?',
    ':SENS:SWE:TIME?',
    # ':DISP:WIND:TRAC:Y:RLEV?',
    # ':DISP:WIND:TRAC:Y:SPAC?',
    # ':DISP:WIND:TRAC:Y:SCAL:PDIV',
    ':UNIT:POW?',
    ':TRACe1:MODE?',
    ':TRACe2:MODE?',
    ':TRACe3:MODE?',

    ':INITiate:CONTinuous?',
    
    ':SYSTem:ERRor:NEXT?',
    # ':OUTPut:STATe?',
    
]:
    print('{}  :  {}'.format(q, inst.query(q)))

*IDN?  :  Keysight Technologies,N9030B,MY56320666,A.20.25
:FORM?  :  ASC,8
:INST:SEL?  :  SA
:SENS:BWID:RES?  :  3.000000000E+06
:SENS:BWID:VID?  :  5.000000000E+07
:SENS:SWE:TIME?  :  4.250000000E-02
:UNIT:POW?  :  DBM
:TRACe1:MODE?  :  WRIT
:TRACe2:MODE?  :  BLAN
:TRACe3:MODE?  :  BLAN
:INITiate:CONTinuous?  :  1
:SYSTem:ERRor:NEXT?  :  +64,"Align Now All required - DETECTED"

yyy = inst.query_ascii_values(':TRAC:DATA? TRACE1')


x = np.linspace(float(inst.query('SENS:FREQ:STAR?')), float(inst.query('SENS:FREQ:STOP?')), int(inst.query('SENS:SWEEP:POINts?')))
inst.write(f'SENS:FREQ:STAR {1e9}')
inst.write(f'SENS:FREQ:STOP {40e9}')
inst.write(f'SENS:SWEEP:POINts {391}')


x = np.linspace(float(inst.query('SENS:FREQ:STAR?')), float(inst.query('SENS:FREQ:STOP?')), int(inst.query('SENS:SWEEP:POINts?')))
y3 = np.array(inst.query_ascii_values(':TRAC:DATA? TRACE2'))


p = figure(title='bar', x_axis_label='Frequency (MHz)', y_axis_label='dBm', width=1440)  #, sizing_mode='scale_width')  # width=1800, height=900)
    
p.line(x/1e6, y3, legend='Gain (dB)', color='blue', alpha=1, line_width=2)
# line(x/1e6, y5, legend='UUT', color='black', alpha=1, line_width=2)
p.line(x/1e6, y3, legend='Ref', color='blue', alpha=1, line_width=2)

# p.line(x/1e6, y6, legend='bar', color='black', alpha=1, line_width=2)


p.legend.location = "top_right"
p.legend.click_policy="hide"
p.legend.background_fill_color = "black"
p.legend.background_fill_alpha = 0.25

p.ygrid.minor_grid_line_color = 'black'
p.ygrid.minor_grid_line_alpha = 0.1

p.xgrid.minor_grid_line_color = 'black'
p.xgrid.minor_grid_line_alpha = 0.1
# p.background_fill_color = "gray"

# p.background_fill_alpha = 0.2

target = show(p, notebook_handle=True)  # show(p)

'''