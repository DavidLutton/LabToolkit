
if read.startswith(b'\x02') == True:
data = bytes.decode(read)
#print(data)
# sample = b'\x0201041102330410\r'

# sample = b'\x0201041102040606\r'
# 020.4 C
Bit = {
    'D15'  : data[0],
    'D14'  : data[1],
    'D13'  : data[2],
    'D12'  : data[3],
    'D11'  : data[4],
    'D10'  : data[5],
    'D9'   : data[6],
    'D8'   : data[7],
    'D7'   : data[8],
    'D6'   : data[9],
    'D5'   : data[10],
    'D4'   : data[11],
    'D3'   : data[12],
    'D2'   : data[13],
    'D1'   : data[14],
    'D0'   : data[15],
}
Value = {
    'Humidity'      : Bit['D4']+Bit['D3']+Bit['D2']+'.'+Bit['D1'],
    #'Temperature'   : Bit['D5']+Bit['D6']+Bit['D7']+Bit['D8'],
    'Temperature'   : Bit['D8']+Bit['D7']+Bit['D6']+'.'+Bit['D5'],
    'Udp'           : Bit['D9'],
    'Ldp'           : Bit['D10'],
    'USym'          : Bit['D11']+Bit['D12'],
    'LSym'          : Bit['D13'],
    'CPolarity'     : Bit['D14'],
}

