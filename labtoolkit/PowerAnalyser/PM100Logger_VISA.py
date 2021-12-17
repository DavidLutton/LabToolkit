import time
import visa
import requests


# rm = visa.ResourceManager('')

# inst = rm.open_resource('GPIB1::13::INSTR', read_termination='\n', write_termination='\n')  # , , **kwargs)
'''with open('PM100_log.csv', 'a') as f:
    while True:
        time.sleep(1)
        Hz = float(inst.query(':FNC:FRQ?'))
        V = float(inst.query(':FNC:VLT?'))
        print('{} Volts AC, {} Hz'.format(V, Hz))
        f.write('{},{}\n'.format(V, Hz))
'''
'''
def send(datum, value):
    payload = "{0!s} value={1!s}".format(datum, value)
    try:
        r = requests.post("http://192.168.57.103:8086/write?db=VHz", data=payload)
        # print(r.status_code)
    except requests.exceptions.ConnectionError:
        print("Failed to Connect to InfluxDB")

while True:
    time.sleep(1)
    Hz = float(inst.query(':FNC:FRQ?'))
    V = float(inst.query(':FNC:VLT?'))
    print('{} Volts AC, {} Hz'.format(V, Hz))
    if V > 64:
        send('Voltage', V)
    send('Frequency', Hz)

        
'''