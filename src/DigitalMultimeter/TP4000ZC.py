
# http://www.multimeterwarehouse.com/TP4000ZC/TP4000ZC_serial_protocol.pdf

import _maps as MAP

def main(data):
    NIBBLE_ALIGN = {
        1   : data[0:4],
        2   : data[8:12],
        3   : data[16:20],
        4   : data[24:28],
        5   : data[32:36],
        6   : data[40:44],
        7   : data[48:52],
        8   : data[56:60],
        9   : data[64:68],
        10  : data[72:76],
        11  : data[80:84],
        12  : data[88:92],
        13  : data[96:100],
        14  : data[104:108],
}
    #print(NIBBLE_ALIGN)
#    for the in NIBBLE_ALIGN:
 #       print(str(the)+" = "+str(NIBBLE_ALIGN[the]))

    ALIGN = -1
    ALIGN = 0
    for ALIGNS in range(1,15):
        if ( ALIGNS == int( NIBBLE_ALIGN[ ALIGNS] ,2 ) ):
            ALIGN += 1
    
    if ( ALIGN != 14 ):
        raise "Data Not Aligned"
    else:
        True
        #print("Aligned")
        
    NIBBLE_DMM = {
        1   : data[4:8],
        2   : data[12:16],
        3   : data[20:24],
        4   : data[28:32],
        5   : data[36:40],
        6   : data[44:48],
        7   : data[52:56],
        8   : data[60:64],
        9   : data[68:72],
        10  : data[76:80],
        11  : data[84:88],
        12  : data[92:96],
        13  : data[100:104],
        14  : data[108:112],
}

    DMM = {
    'AC'      : int( NIBBLE_DMM[1][0:1] ,2 ),
    'DC'      : int( NIBBLE_DMM[1][1:2] ,2 ),
    'AUTO'    : int( NIBBLE_DMM[1][2:3] ,2 ),
    'RS232'   : int( NIBBLE_DMM[1][3:4] ,2 ),

    'SIGN'    : MAP.SIGN [ int( NIBBLE_DMM[2][0:1] ,2) ],
    '7-1'     : MAP.DIGIT [ NIBBLE_DMM[2][1:4] + NIBBLE_DMM[3][0:4] ],
    'D-1'     : MAP.DECIMAL [ int( NIBBLE_DMM[4][0:1] ,2 ) ],
    '7-2'     : MAP.DIGIT [ NIBBLE_DMM[4][1:4] + NIBBLE_DMM[5][0:4] ],
    'D-2'     : MAP.DECIMAL [ int( NIBBLE_DMM[6][0:1] ,2 ) ],
    '7-3'     : MAP.DIGIT [ NIBBLE_DMM[6][1:4] + NIBBLE_DMM[7][0:4] ],
    'D-3'     : MAP.DECIMAL [ int( NIBBLE_DMM[8][0:1] ,2 ) ],
    '7-4'     : MAP.DIGIT [ NIBBLE_DMM[8][1:4] + NIBBLE_DMM[9][0:4] ],

    'Micro'   : NIBBLE_DMM[10][0:1],
    'Nano'    : NIBBLE_DMM[10][1:2],
    'Kilo'    : NIBBLE_DMM[10][2:3],
    'Diode'   : NIBBLE_DMM[10][3:4],

    'Mili'    : NIBBLE_DMM[11][0:1],
    'Duty'    : NIBBLE_DMM[11][1:2],
    'Mega'    : NIBBLE_DMM[11][2:3],
    'Sound'   : NIBBLE_DMM[11][3:4],

    'Farads'  : NIBBLE_DMM[12][0:1],
    'Ohms'    : NIBBLE_DMM[12][1:2],
    'Rel'     : NIBBLE_DMM[12][2:3],
    'Hold'    : NIBBLE_DMM[12][3:4],

    'Amps'    : NIBBLE_DMM[13][0:1],
    'Volts'   : NIBBLE_DMM[13][1:2],
    'Hertz'   : NIBBLE_DMM[13][2:3],
    'Battery' : NIBBLE_DMM[13][3:4],

    'Celsius' : NIBBLE_DMM[14][1:2],
}

    for unit in ['Farads','Ohms','Amps','Volts','Hertz','Celsius','Duty']:
        if DMM[unit] == b"1":
            DMM["Unit"] = unit
  
    DMM["Prefix"] = ""
    for scale in ['Micro','Mega','Kilo','Mili','Nano']:
        if DMM[scale] == b"1":
            DMM["Prefix"] = scale

    DMM["Current"] = ""
    for current in ['AC','DC']:
        if DMM[current] == b"1":
            DMM["Current"] = current


    DMM["Relative"] = ""
    for rels in ['Rel']:
       if DMM[rels] == b"1":
           DMM["Relative"] = rels

#    for the in DMM:
 #       print(the+" = "+str(DMM[the]))

    return {
        "Digits" : str(DMM['7-1']) + DMM['D-1']+ str(DMM['7-2']) +DMM['D-2']+str( DMM['7-3']) +DMM['D-3']+str(DMM['7-4']),
	"Prefix" : DMM["Prefix"],
	"Unit"   : MAP.UNIT[ DMM["Unit"] ],
	"Sign"   : DMM["SIGN"],
	"DMM" : { 
		'AC'      : DMM['AC'],
		'DC'      : DMM['DC'],
		'RS232'   : DMM['RS232'],
		'AUTO'    : DMM['AUTO'],
		'Diode'   : DMM['Diode'],
		'Sound'   : DMM['Sound'],
		'Rel'     : DMM['Rel'],
		'Hold'    : DMM['Hold'],
		'Battery' : DMM['Battery'],
   }	
}

