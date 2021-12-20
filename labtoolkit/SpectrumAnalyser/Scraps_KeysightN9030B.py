
print(inst.query('*IDN?'))
print(inst.query('*OPT?').split(','))

Keysight Technologies,N9030B,
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
'''
*IDN?  :  Keysight Technologies,N9030B
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

'''