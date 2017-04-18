import visa
from pprint import pprint
import time

rm = visa.ResourceManager()


HP437B = rm.open_resource('GPIB0::11::INSTR')
assert HP437B.query('*IDN?').startswith('HEWLETT-PACKARD,437B,')


GEN = rm.open_resource('GPIB0::3::INSTR')
assert GEN.query('*IDN?').startswith('Hewlett-Packard, ESG-4000B, MY41000406, B.03.8')


def level(wantedlevel = -3.0):



    presentlevel = float(HP437B.query('?'))
    print(presentlevel)

    leveldelta = wantedlevel - presentlevel
    print(leveldelta)

    levelcurrent = float(GEN.query("POWer:LEVel?"))

    print(levelcurrent)

    levelnew = levelcurrent + leveldelta
    try:
        error = (leveldelta / levelcurrent) * 100
    except ZeroDivisionError:
        error = 0
    print(error)

    print()
    print()
    levellimit = -3
    if input("level new " + str(levelnew)) == "y":
        if levelnew > levellimit:
            print("over limit")

            GEN.write("POWer:LEVel " + str(levellimit) + "dBm")
        else:
            GEN.write("POWer:LEVel " + str(levelnew) + "dBm")



level(wantedlevel = 33)
time.sleep(1)
level(wantedlevel = 33)

'''
:DIAGnostic[:CPU]:INFOrmation:OTIMe?

:FREQuency[:CW] <val><unit>
:FREQuency[:CW]?
:FREQuency:MODE CW|FIXed|LIST
:FREQuency:MODE?
:OUTPut:MODulation[:STATe] ON|OFF|1|0
:OUTPut:MODulation[:STATe]?
:OUTPut[:STATe] ON|OFF|1|0
:OUTPut[:STATe]?

:POWer:ATTenuation:AUTO ON|OFF|1|0
:POWer:ATTenuation:AUTO?
:UNIT:POWer DBM|DBUV|V|VEMF|
:UNIT:POWer?



'''
