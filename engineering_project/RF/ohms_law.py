#!/usr/bin/env python3

from pint import UnitRegistry

ureg = UnitRegistry()
# ureg.default_format = '~P'


def VIR(I, R):  # V=I*R
    return((I * R).to(ureg.volt))


def test_VIR():
    assert VIR(20 * ureg.amp, 8 * ureg.ohm) == 160 * ureg.volt


def VPI(P, I):  # V=P/I
    return((P / I).to(ureg.volt))


def test_VPI():
    assert VPI(20 * ureg.watt, 8 * ureg.amp) == 2.5 * ureg.volt


def VPR(P, R):  # V=SQRT(P*R)
    return((P * R) ** .5).to(ureg.volt)


def test_VPR():
    assert VPR(8 * ureg.watt, 50 * ureg.ohm) == 19.999999999999996 * ureg.volt


def IVR(V, R):  # I=V/R
    return((V / R).to(ureg.amp))


def test_IVR():
    assert IVR(10 * ureg.volt, 50 * ureg.ohm) == 0.2 * ureg.amp


def IPR(P, R):  # I=SQRT(P/R)
    return(((P / R) ** 0.5).to(ureg.amp))


def test_IPR():
    assert IPR(10 * ureg.watt, 50 * ureg.ohm) == 0.44721359549995787 * ureg.amp


def IPV(P, V):  # I=P/V
    return((P / V).to(ureg.amp))


def test_IPV():
    assert IPV(10 * ureg.watt, 10 * ureg.volt) == 1 * ureg.amp


def PVI(V, I):  # P=V*I
    return((V * I).to(ureg.watt))


def test_PVI():
    assert PVI(10 * ureg.volt, 10 * ureg.amp) == 100 * ureg.watt


def PIR(I, R):  # P=I²*R
    return((I ** 2 * R).to(ureg.watt))


def test_PIR():
    assert PIR(1 * ureg.amp, 50 * ureg.ohm) == 50 * ureg.watt


def PVR(V, R):  # P=V²/R
    return((V ** 2 / R).to(ureg.watt))


def test_PVR():
    assert PVR(17.99 * ureg.volt, 50 * ureg.ohm) == 6.472801999999999 * ureg.watt


def RVP(V, P):  # R=V²/P
    return((V ** 2 / P).to(ureg.ohm))


def test_RVP():
    assert RVP(17.99 * ureg.volt, 6.472801999999999 * ureg.watt) == 50 * ureg.ohm


def RPI(P, I):  # R=P/I²
    return((P / I ** 2).to(ureg.ohm))


def test_RPI():
    assert RPI(10 * ureg.watt, 1 * ureg.amp) == 10 * ureg.ohm


def RVI(V, I):  # R=V/I
    return((V / I).to(ureg.ohm))


def test_RVI():
    assert RVI(10 * ureg.volt, 1 * ureg.amp) == 10 * ureg.ohm
