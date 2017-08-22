"""RFPy - RF calculations in Python."""

import functools
import pint
import numpy as np


'''
BS EN 61000-4-6:2014
Conducted Immunity Cal                         150
SigGen - Cable - Amp - Cable - Sampler - Pad - CDN
                                Cable          100
                                Pad            Pad(s)
                                Head           Head
                                Meter          Meter
'''
'''
Conducted Immunity Test                        AE
SigGen - Cable - Amp - Cable - Coupler - Pad - CDN
                                Cable          EUT
                                Pad
                                Head
                                Meter
'''

'''
BS EN 61000-4-3:2006+A2:2010
Radiated Immunity Cal
SigGen - Cable - Amp - Cable - Coupler - Antenna - )) (( - Field Strength Meter
                               Cable
                               Pad
                               Head
                               Meter
'''
'''
Radiated Immunity Test
SigGen - Cable - Amp - Cable - Coupler - Antenna - )) (( - Field Strength Meter
                               Cable
                               Pad
                               Head
                               Meter
'''
ureg = pint.UnitRegistry()
ureg.default_format = '~P'
Q_ = ureg.Quantity


# ureg.define('emf = 0.5 * volt = e.m.f')  # half of one volt is one emf
ureg.define('emf = 0.5 * volt')  # half of one volt is one emf
ureg.define('dB = []')
ureg.define('dBm = []')
# uref.define('dBu = 0.7746 volt')  # log20
# uref.define('dBV = 1 volt')  # log20


'''ureg.define("dBW = []")  # Referenced to 1 Watt
ureg.define("dBk = dBW; offset: + 30")    # Referenced to 1 KW or offset + 30 dBW
ureg.define("dBm = dBW; offset: - 30")
ureg.define("dBuW = dBW; offset: - 60 = dBµW")
ureg.define("dBpW = dBW; offset: - 120")
'''
# ureg.define('dBW = (10 ** ( watt / 10 ))')


class CorrectionFactor(object):
    """."""

    def __init__(self, FrequencyPoints, ):
        """."""
        self.FrequencyPoints = FrequencyPoints  # x
        self.CorrectionFactor = CorrectionFactor  # y
        # self.interpolation


class Trace(object):
    """."""

    def __init__(self, typex='LogFrequency', points=801, start=300e3, stop=6e9, *, frequencypoints=False):
        return NotImplemented

        '''if sweeptype == 'LOG':
            sweep = np.geomspace(start, stop, points)
        elif sweeptype == 'LIN':
            sweep = np.linspace(start, stop, points)
        elif sweeptype == 'List':
            sweep = frequencypoints

        return sweep
        '''


@functools.lru_cache(maxsize=1024, typed=False)
def log20(value):
    """."""
    return np.log(20**value)/np.log(20)


@functools.lru_cache(maxsize=1024, typed=False)
def dBofVratio(ratio):
    """Calculate the dB equivalent of the voltage ratio."""
    return Q_(20*np.log10(ratio), 'dB')  # ratio(dB)


@functools.lru_cache(maxsize=1024, typed=False)
def VofdB(dB):
    return 10.**(dB/20.)


@functools.lru_cache(maxsize=1024, typed=False)
def dBofPratio(ratio):
    """Calculate the dB equivalent of the power ratio.

    Useful for correcting readings from rf power heads"""
    return Q_(10*np.log10(ratio), 'dB')  # ratio(dB)


@functools.lru_cache(maxsize=1024, typed=False)
def correctpowerreadingwithfactor(reading, factor, *, units='dBm'):
    """."""
    return Q_(reading - dBofPratio(factor), units)


@functools.lru_cache(maxsize=1024, typed=False)
def calibrationlevel(*, TestLevel=10, Margin=1.025, ModulationIndex=1.8, Units='emf'):
    testlevel = Q_(TestLevel, Units) * Margin
    # print('TestLevel {}'.format(testlevel))
    callevel = testlevel * ModulationIndex
    # print('CalLevel {}'.format(callevel))
    return(callevel)


def test_correctpowerreadingwithfactor():
    assert correctpowerreadingwithfactor(10, 0.50) == Q_(13.010299956639813, 'dBm')
    assert correctpowerreadingwithfactor(10, 0.25) == Q_(16.020599913279625, 'dBm')
    assert correctpowerreadingwithfactor(0, 4) == Q_(-6.020599913279624, 'dBm')
    assert correctpowerreadingwithfactor(0, 2) == Q_(-3.010299956639812, 'dBm')
    assert correctpowerreadingwithfactor(0, 1) == Q_(0, 'dBm')
    assert correctpowerreadingwithfactor(0, 0.50) == Q_(3.010299956639812, 'dBm')
    assert correctpowerreadingwithfactor(0, 0.25) == Q_(6.020599913279624, 'dBm')
    assert correctpowerreadingwithfactor(-10, 0.50) == Q_(-6.9897000433601875, 'dBm')
    assert correctpowerreadingwithfactor(-10, 0.25) == Q_(-3.979400086720376, 'dBm')


@functools.lru_cache(maxsize=1024, typed=False)
def requiredforwardpowerfromVcal(*, ForwardPowerdBm, CalibrationLevel, TargetLevel):
    """."""
    # return Q_(ForwardPowerdBm+dBofVratio(TargetLevel/CalibrationLevel), 'dBm')

    # Given a forward power of 38dBm for 18.45 emf calculate forward power for 10.25 emf
    # print('{:.2f}'.format(Q_(38.74+dBofVratio(10.25/18.45), 'dBm')))

    return Q_(round(ForwardPowerdBm + dBofVratio(TargetLevel/CalibrationLevel), 2), 'dBm')


@functools.lru_cache(maxsize=1024, typed=False)
def wattstovolts(watts, *, ohms=50):
    """."""
    return np.sqrt(Q_(watts, 'W')*Q_(ohms, 'ohm')).to('V')


@functools.lru_cache(maxsize=1024, typed=False)
def wattstodBm(watts):
    return Q_(10 * np.log10((watts / 0.001)), 'dBm')


@functools.lru_cache(maxsize=1024, typed=False)
def dBmtowatts(dBm):
    return Q_(10 ** ((dBm - 30)/10), 'W')


@functools.lru_cache(maxsize=1024, typed=False)
def wattstoemf(watts, *, ohms=50):
    """."""
    return np.sqrt(Q_(watts, 'W')*Q_(ohms, 'ohm')).to('emf')


@functools.lru_cache(maxsize=1024, typed=False)
def emftowatts(emf, *, ohms=50):
    return ((Q_(emf, 'emf').to('V')) ** 2 / Q_(ohms, 'ohms')).to('W')


def test_emfwattsequilivence():
    wattstoemf(3.141) == emftowatts(wattstoemf(3.141).magnitude)
    emftowatts(3.141) == wattstoemf(emftowatts(3.141).magnitude)


def test_testemfequilivence():
    assert Q_(10, 'emf') * 1.8 == Q_(18, 'emf')
    assert Q_(10, 'emf') * 1.8 == Q_(18.0, 'emf')
    assert Q_(20, 'emf') * 1.8 == Q_(36, 'emf')
    assert Q_(20.0, 'emf') * 1.8 == Q_(36, 'emf')


def test_wattstovolts():
    assert wattstovolts(2) == Q_(9.999999999999998, 'V')


def test_wattstoemf():
    assert wattstoemf(2) == Q_(19.999999999999996, 'emf')


def test_dBofVratio():
    assert dBofVratio(float(18/10)) == 5.105450102066121
    assert dBofVratio(float(10/18)) == -5.10545010206612

    assert dBofVratio(float(10/9.4)) == 0.5374429280060267
    # Wanted level is 10 volts, measured level is 9.4
    # What amount of power (dB) change is required to get to wanted level

    assert dBofVratio(float(10/11)) == -0.8278537031645011
    # Wanted level is 10 volts, measured level is 11
    # What amount of power (dB) change is required to get to wanted level

    assert dBofVratio(float(10/9.94)) == 0.05227231205373506


def test_wattstoemf():
    # emf =
    assert wattstoemf(0.189) * 3 == Q_(18.444511378727274, 'emf')  # For CDNs
    # assert wattstoemf(0.189, ohms=150) == Q_(18.444511378727274, 'emf')  # For CDNs
    assert wattstoemf(0.147) == Q_(5.422176684690383, 'emf')  # For Clamps

    # print('{:.3f}'.format(wattstoemf(watts)))  # For Clamps


# lg = LogConverter()
# watts = Q_(6.42, 'watt')
# print(watts)
'''dBW = Q_(-30, 'dBW')
print(dBW)
dBm = dBW.to(ureg.dBm)
print(dBm)

dBm = Q_(-30, 'dBm')
print(dBm)
dBW = dBm.to(ureg.dBW)
print(dBW)'''
# dBW = lg.to_reference(value=watts)
# print(dBW)
# print(lg.from_reference(value=dBW))
# print(lg.from_reference(value=dBm.to(ureg.dBW)))
# print(lg.from_reference(value=dBm))


# ? print(dBW + (10 * ureg.dB))


'''print('\n\tWatts to dBm')
for case in 0.00001, 0.0001, 0.001, 1.0, 10, 50, 100, 200, 500, 977.23722, 1000:
    value = (10 * log10((Q_(case, 'watt')).magnitude / 0.001))
    print('{:.5f} Watts --> {:.2f} dBm'.format(case, value))

print('\n\tdBm to Watts')
for case in -30, -20, -10, 0.0, 10, 20, 30, 40, 50, 59.9, 60, 63, 66, 69, 70, 72, 80:
    value = (10 ** ((case - 30)/10))
    print('{} dBm --> {:.6f}'.format(case, Q_(value, 'watt')))

print('\n\tVolts to Watts in 50 Ohms')
for case in 3.0, 5.4, 10, 18, 28, 38:
    value = (Q_(case, 'volt') ** 2 / Q_(50, 'ohm')).to('watt')
    print('{} Volts --> {}'.format(case, value))

print('\n\tWatts to Volts in 50 Ohms')
for case in 2.0, 6.48, 15.68, 28.88:
    value = ((Q_(50, 'ohm') * Q_(case, 'watt')) ** 0.5).to('volt')
    print('{} Watts --> {:.3f}'.format(case, value))

'''
'''
ureg.load_definitions('FrequencyRegistry.txt')

with ureg.context('rf'):
    Z = (ureg.ohm * 50)

    q = (20 * ureg.cm)
    print(q.to('MHz'))

    q = (230 * ureg.MHz)
    print(q.to('cm'))


'''
'''
#!/usr/bin/env python3

import numpy as np
from pint import UnitRegistry
from pint.unit import UnitDefinition
from pint.converters import Converter


class LogConverter(Converter):
    is_multiplicative = False

    def to_reference(self, value, inplace=False):
        return value

    def from_reference(self, value, inplace=False):
        return value

ureg = UnitRegistry()
ureg.default_format = '~P'
ureg.load_definitions('FrequencyRegistry.txt')

with ureg.context('rf'):
    Z = (ureg.ohm * 50)

    q = (20 * ureg.cm)
    print(q.to('MHz'))

    q = (230 * ureg.MHz)
    print(q.to('cm'))

    q = (8000 * ureg.Hz)
    print(q.to('km'))

    print()
    q = 20 * ureg.dBm
    print(q)
    print(q.magnitude)
    res = (10 ** ((q - 30)/10)) * ureg.watt
    print(res)

    print()
    q = 10 * ureg.watt
    print(q)
    print(q.magnitude)
    res = (10 * np.log10(q.magnitude / 0.001)) * ureg.dBm
    print(res)

    print()
    print("18V")
    q = ((18 * ureg.volt) ** 2 / Z).to('W')
    print(q)
    print(q.magnitude)
    res = (10 * np.log10(q.magnitude / 0.001)) * ureg.dBm
    print(res)

'''
'''

def V2dBm(V, *, R=50):
    # return(10. * np.log10(V * ureg.volt ** 2. / R * ureg.ohm) + 30)
    return(10. * np.log10(V ** 2. / R) + 30)


def dBm2W(dBm):
    return((10. ** ((dBm - 30)/10)) * ureg.watt)

def W2dBm(W):
    return(10 * np.log10(W / 0.001))
    # return(10 * np.log10(W * ureg.watt / 0.001))


def p(func, v):  # Present
    ret = func(v)
    print(func.__name__ + " " + str(v) + "  " + str(ret))
    return(ret)

for x in [-20, -10, 0, 3, 6, 10, 20, 30, 40, 50, 60, 70]:
    print()
    print(str(x) + " dBm")
    p(W2dBm, p(dBm2W, p(V2dBm, p(W2V, p(dBW2W, p(W2dBW, p(dBm2W, x).magnitude)).magnitude).magnitude)).magnitude)
'''
'''
# http://www.rapidtables.com/convert/power/dBm_to_Watt.htm
with ureg.context('sp'):
    q = (0.3 * ureg.m)
    print(q.to('MHz'))

    # print(dir(np))

    # print(dir(pint))
'''
'''
with ureg.context('sp'):
    q = 128 * ureg.MHz
    print(q)
    print(q.magnitude)
    print(q.units)
    # print(dir(np))
    # print(dir(pint))
'''

'''
accel = 1.3 * ureg['meter/second**2']
print('The pretty representation is {:P}'.format(accel))
print('The str is {:~}'.format(accel))
print('The pretty susscient representation is {:~P}'.format(accel))

'''
# https://en.wikipedia.org/wiki/File:Ohms_law_wheel_WVOA.svg
# eg http://www.ohmslawcalculator.com/ohms-law-calculator


######
'''
print(Q_(9, 'V').to('emf'))
# Q_(9, 'V')

callevel = Q_(18, 'emf')
wantedlevel = Q_(10, 'emf')


R = float(callevel/wantedlevel)  # R

RdB = dBofVratio(R)

print(RdB)
print('...')
factor = Q_(40.6, 'dBm')
print('Power at coupler {}'.format((factor)))
print('Power applied to CDN {}'.format((factor)-Q_(6, 'dB')))
print()
print('diff')
print('Power at coupler {}'.format((factor-RdB)))
print('Power applied to CDN {}'.format((factor-RdB)-Q_(6, 'dB')))

# Observing device is 50Ohm but the connection path is 150Ohm, therefore the  50Ohm device observes a third of the total power
'''
'''
Stress.Formula=7*x+15.6
Stress.Formula=SQR(x*50)*2
Stress.Formula=SQR(x*50)*6
Stress.Formula=x+26
Stress.Formula=X*6
'''


'''print('{:.02fP}'.format(Q_(20, 'V').plus_minus(.01)))
print(Q_(20, 'V').plus_minus(.01))

print(dBofVratio(float(18/10)))
print(dBofVratio(float(18/10)))
print(float(18/10))


watts = 0.147
# print(voltsin50ohmfromwatts(watts))
# print(emfin150ohmfromvoltsin50ohmvia100ohm(voltsin50ohmfromwatts(watts)))
# print('{:.3f}'.format(wattstoemf(watts)*3))  # For CDNs
# print('{:.3f}'.format(wattstoemf(watts)*3))  # For CDNs
print('{:.3f}'.format(wattstoemf(.74)*3))  # For CDNs
# print('{:.3f}'.format(wattstoemf(watts)))  # For Clamps
# print('{:.3f}'.format(wattstoemf(watts)))  # For Clamps
print('{:.3f}'.format(wattstoemf(6.66)))  # For Clamps

# print(wattstoemf.cache_info())

print(emftowatts(18.35/3))  # For CDNs
print(emftowatts(18.35))  # For Clamps
'''


'''print(10*np.log10(1e3))
http://www.eevblog.com/forum/rf-microwave/from-dbm-to-dbmhz/
First order, rough approximation would be to take your dBm reading and subtract the log
value of the RBW used for the measurement.  For example, if you use 1kHz RBW in your
analyzer, and you measure -90dBm, then:

dBm/Hz = -90dBm - 10LOG(1kHz)

-120dBm/Hz (approximate)
'''


def VSWR2RL(VSWR):
    return(-20 * np.log10((VSWR - 1) / (VSWR + 1)))


def RL2VSWR(RL):
    return((10 ** (RL / 20) + 1) / (10 ** (RL / 20) - 1))


def test_RL2VSWR():
    assert RL2VSWR(30) == 1.0653108640674351
    assert RL2VSWR(60) == 1.002002002002002
    assert RL2VSWR(0.5) == 34.75315212699187


def test_VSWR2RL():
    assert VSWR2RL(1.2) == 20.827853703164504
    assert VSWR2RL(1.002) == 60.00868154958637
    assert VSWR2RL(100) == 0.17372358370185334


def VSWR2Refl(VSWR):  # ectionCoefficient
    return((VSWR - 1)/(VSWR + 1))


def test_VSWR2Refl():
    assert VSWR2Refl(1.50) == 0.2


'''
 Γ=10(‐ReturnLoss/20)
 VSWR=(1+|Γ|)/(1‐|Γ|)
 MismatchLoss(dB)=10log(Γ**2)
 ReflectedPower(%)=100*Γ **2
 ReturnLoss(dB)= ‐20log|Γ|
 Γ=(VSWR‐1)/(VSWR+1)
 ThroughPower(%)=100(1‐Γ2)
'''
'''with ureg.context('sp'):
    Q = Q_(27.5, 'cm')
    print(Q.to('MHz'))
    print(Q.to('MHz')/2)
    print(Q.to('MHz')/4)
    print(Q.to('MHz')/8)
    print(Q.to('MHz')/16)
    print(Q.to('MHz')/32)
    print(Q.to('MHz')/64)
    print(Q.to('MHz')/128)
    print()
'''

'''def decimalplace(x, y):
    # z = "{0:." + "{}".format(x) + "f~P}"
    return(("{0:." + "{}".format(x) + "f~P}").format(y))

dp = decimalplace
'''

'''
    q = (Z * Q_(6.432, 'watt')) ** 0.5
    print(q)
    print(q.to('V'))
'''
'''
    print()
    print("18V")
    q = Q_(18, 'volt') ** 2 / Z
    print(q)
    print(q.to('W'))
'''
'''
    print()
    q = Q_(20, 'dBm')
    print(q)
    print(q.magnitude)
    res = (10 ** ((q - 30)/10)) * ureg.watt
    print(res)
'''
'''
    print()
    q = Q_(10, 'watt')
    print(q)
    print(q.magnitude)
    res = (10 * np.log10(q.magnitude / 0.001)) * ureg.dBm
    print(res)
'''
'''
    print()
    print("18V")
    q = (Q_(18, 'volt') ** 2 / Z).to('W')
    print(q)
    print(q.magnitude)
    res = (10 * np.log10(q.magnitude / 0.001)) * ureg.dBm
    print(res)
'''
'''
    print()
    q = 1 / Q_(5*60, 'seconds')
    print(q)
    print(dp(6, q.to('Hz')))
    print(dp(6, q.to('mHz')))
'''
