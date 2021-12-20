import visa
import time
# start of Untitled

rm = visa.ResourceManager()
E4418B_25 = rm.open_resource('GPIB0::25::INSTR')
E4418B_25.write(':SENSe:FREQuency:CW %G MHZ' % (55.0))
#E4418B_25.write(':SENSe:FREQuency:CW %G HZ' % (265000000000.0))
#string = E4418B_25.query(':SENSe:CORRection:CSET:SELect?')
#temp_values = E4418B_25.query_ascii_values(':SENSe:CORRection:CSET:STATe?')
#boolean = int(temp_values[0])


#date = E4418B_25.query(':SERVice:SENSor:CDATe?')
#place = E4418B_25.query(':SERVice:SENSor:CPLace?')
#string1 = E4418B_25.query(':MEMory:TABLe:SELect?')
#data = E4418B_25.query(':MEMory:CATalog:ALL?')
temp_values = E4418B_25.query_ascii_values(':FETCh:SCALar:POWer:AC?')
ac = temp_values[0]
print(ac)
#amplitude_unit = E4418B_25.query(':UNIT:POWer?')
#print(amplitude_unit)

E4418B_25.close()
rm.close()

# end of Untitled
