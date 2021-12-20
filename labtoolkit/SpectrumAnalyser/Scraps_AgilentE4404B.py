
self.write(':SYST:ERR:VERB 1')
self.write(':CAL:AUTO 0')


'''
ana.write(w)

for q in [
'*IDN?',
# '*CAL?',
':FORM?',
':INST:SEL?',
# ':SENS:FREQ:STAR?',
# ':SENS:FREQ:STOP?',s
':SENS:BWID:RES?',
':SENS:BWID:VID?',
':SENS:SWE:TIME?',
# ':DISP:WIND:TRAC:Y:RLEV?',
# ':DISP:WIND:TRAC:Y:SPAC?',
# ':DISP:WIND:TRAC:Y:SCAL:PDIV',
':UNIT:POW?',
':TRACe1:MODE?',
':INITiate:CONTinuous?',
':SYSTem:ERRor:NEXT?',
':OUTPut:STATe?',
# ':SOURce:CORRection:OFFSet?',
':SOURce:POWer:ATTenuation?',
# ':SOURce:POWer:ATTenuation:AUTO?',
':SOURce:POWer:LEVel:IMMediate:AMPLitude?',
':SOURce:POWer:MODE?',
# ':SOURce:POWer:SPAN?',
# ':SOURce:POWer:STARt?',
# ':SOURce:POWer:STEP:AUTO?',
# ':SOURce:POWer:STEP:INCRement?'
# ':SOURce:POWer:SWEep?',
':SOURce:POWer:TRCKing?',
':SENS:FREQ:STAR?',
':SENS:FREQ:STOP?',
# ':SENS:FREQ:POINts?',
':SENS:FREQ:SPAN?',
]:
print(f'{q}  :  {ana.query(q)}', end='')
# :SOURce:POWer:TRCKing:PEAK
# :TRACe1|2|3:MODE WRITe|MAXHold|MINHold|VIEW|BLANk'''
