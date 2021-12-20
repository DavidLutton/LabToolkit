import visa
import time
# start of Untitled

rm = visa.ResourceManager()
E4418B_25 = rm.open_resource('GPIB1::25::INSTR')
E4418B_25.write(':SENSe:FREQuency:CW %G HZ' % (265000000000.0))
string = E4418B_25.query(':SENSe:CORRection:CSET:SELect?')
temp_values = E4418B_25.query_ascii_values(':SENSe:CORRection:CSET:STATe?')
boolean = int(temp_values[0])

date = E4418B_25.query(':SERVice:SENSor:CDATe?')
place = E4418B_25.query(':SERVice:SENSor:CPLace?')
string1 = E4418B_25.query(':MEMory:TABLe:SELect?')
temp_values = E4418B_25.query_ascii_values(':FETCh:SCALar:POWer:AC?')
ac = temp_values[0]

temp_values = E4418B_25.query_ascii_values(':FETCh:SCALar:POWer:AC?')
ac1 = temp_values[0]

amplitude_unit = E4418B_25.query(':UNIT:POWer?')
E4418B_25.write(':OUTPut:ROSCillator:STATe %d' % (0))
temp_values = E4418B_25.query_ascii_values(':OUTPut:ROSCillator:STATe?')
boolean1 = int(temp_values[0])

temp_values = E4418B_25.query_ascii_values(':CALibration:ZERO:AUTO?')
boolean2 = int(temp_values[0])

E4418B_25.write(':CALibration:ZERO:AUTO %s' % ('ONCE'))
E4418B_25.write(':SENSe:FREQuency:CW %G MHZ' % (50.0))
E4418B_25.write(':OUTPut:ROSCillator:STATe %d' % (1))
temp_values = E4418B_25.query_ascii_values(':CALibration1:AUTO?')
calibration = int(temp_values[0])

E4418B_25.write(':CALibration1:AUTO %s' % ('ONCE'))
E4418B_25.close()
rm.close()

# end of Untitled
