import binascii
import visa
import time
import sys
import uuid
import numpy as np
from openpyxl import Workbook
from datetime import datetime

uuiddoc = str(uuid.uuid4())


def main(wb, uuiddoc):
    rm = visa.ResourceManager()
    ws = wb.active
    # print(rm.list_resources())

    # inst = rm.open_resource('GPIB0::11::INSTR')

    # inst.query('IDN?')
    
    while True:
        time.sleep(1)
        now = datetime.utcnow()
        now = datetime.isoformat(now, sep='T')
        now = now.replace(':', '.')

        print(now)

        

        
        #print(str(reading) + " dBm" + ", " + str(loop))
        #ws.append([str(reading), "dBm", str(loop), str(now)])
        #wb.save("Stability-" + uuiddoc + ".xlsx")



if __name__ == "__main__":
    try:
        wb = Workbook()
        main(wb, uuiddoc)
    except KeyboardInterrupt:
        wb.save("PowerAnalyser-" + uuiddoc + ".xlsx")
        print('Received Ctrl-c')
