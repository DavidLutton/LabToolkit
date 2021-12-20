import binascii
import visa
import time
import numpy as np
rm = visa.ResourceManager()
# print(rm.list_resources())

inst = rm.open_resource('GPIB0::11::INSTR')

inst.write('*IDN?')
# time.sleep(.1)
# inst.read()
print(inst.read().strip())


print()
z = 50
while True:
    time.sleep(1)

    # inst.write("EX")
    reading = float(inst.query('?'))

    volts = np.sqrt(z * 10. ** (float(reading) / 10. - 3))
    watts = (float(volts) ** 2) / z

    print(str(reading) + " dBm")
    print("%.4f V" % volts)
    print("%.4f W" % watts)
    print("%.4f mW" % float(watts * 1000))

    '''inst.write("LP2")
    binstate = inst.read_raw()
    binstate = binstate[2:]
    print(len(binstate[40:48]))
    print(binstate[40:48])
    binascii.b2a_uu(binstate[40:48])
    '''
    # cf = "KB" + input("Cal Factor:") + "EN"
    # print(cf)
    # inst.write(cf)

    # inst.write("DUHello Dave")
    # print(inst.read())
    # inst.write("EX")
    

print()
z = 50
while True:
    time.sleep(1)

    # inst.write("EX")
    reading = float(inst.query('?'))

    volts = np.sqrt(z * 10. ** (float(reading) / 10. - 3))
    watts = (float(volts) ** 2) / z

    print(str(reading) + " dBm")
    print("%.4f V" % volts)
    print("%.4f W" % watts)
    print("%.4f mW" % float(watts * 1000))

    '''inst.write("LP2")
    binstate = inst.read_raw()
    binstate = binstate[2:]
    print(len(binstate[40:48]))
    print(binstate[40:48])
    binascii.b2a_uu(binstate[40:48])
    '''
    # cf = "KB" + input("Cal Factor:") + "EN"
    # print(cf)
    # inst.write(cf)

    # HP 437 Operating.pdf P71
    # inst.write("DU123456789012")
    # inst.write("DU       Hello")
    
    # inst.write("DU Who IDNxnnn")
    # inst.write("DU     IDNC031")
    # message = "Hello"
    # inst.write("DU" + message.rjust(12))
    
    # inst.write("DE")



    # inst.write("DE")


