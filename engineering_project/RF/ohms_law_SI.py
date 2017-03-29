#!/usr/bin/env python3

from pint import UnitRegistry

ureg = UnitRegistry()

# ureg.default_format = '~W'


def VAΩ(A, Ω):  # V=A*Ω
    return((A * Ω).to(ureg.volt))


def test_VAΩ():
    assert VAΩ(20 * ureg.amp, 8 * ureg.ohm) == 160 * ureg.volt


def VWA(W, A):  # V=W/A
    return((W / A).to(ureg.volt))


def test_VWA():
    assert VWA(20 * ureg.watt, 8 * ureg.amp) == 2.5 * ureg.volt


def VWΩ(W, Ω):  # V=SQΩT(W*Ω)
    return((W * Ω) ** .5).to(ureg.volt)


def test_VWΩ():
    assert VWΩ(8 * ureg.watt, 50 * ureg.ohm) == 19.999999999999996 * ureg.volt


def AVΩ(V, Ω):  # A=V/Ω
    return((V / Ω).to(ureg.amp))


def test_AVΩ():
    assert AVΩ(10 * ureg.volt, 50 * ureg.ohm) == 0.2 * ureg.amp


def AWΩ(W, Ω):  # A=SQΩT(W/Ω)
    return(((W / Ω) ** 0.5).to(ureg.amp))


def test_AWΩ():
    assert AWΩ(10 * ureg.watt, 50 * ureg.ohm) == 0.44721359549995787 * ureg.amp


def AWV(W, V):  # A=W/V
    return((W / V).to(ureg.amp))


def test_AWV():
    assert AWV(10 * ureg.watt, 10 * ureg.volt) == 1 * ureg.amp


def WVA(V, A):  # W=V*A
    return((V * A).to(ureg.watt))


def test_WVA():
    assert WVA(10 * ureg.volt, 10 * ureg.amp) == 100 * ureg.watt


def WAΩ(A, Ω):  # W=A²*Ω
    return((A ** 2 * Ω).to(ureg.watt))


def test_WAΩ():
    assert WAΩ(1 * ureg.amp, 50 * ureg.ohm) == 50 * ureg.watt


def WVΩ(V, Ω):  # W=V²/Ω
    return((V ** 2 / Ω).to(ureg.watt))


def test_WVΩ():
    assert WVΩ(17.99 * ureg.volt, 50 * ureg.ohm) == 6.472801999999999 * ureg.watt


def ΩVW(V, W):  # Ω=V²/W
    return((V ** 2 / W).to(ureg.ohm))


def test_ΩVW():
    assert ΩVW(17.99 * ureg.volt, 6.472801999999999 * ureg.watt) == 50 * ureg.ohm


def ΩWA(W, A):  # Ω=W/A²
    return((W / A ** 2).to(ureg.ohm))


def test_ΩWA():
    assert ΩWA(10 * ureg.watt, 1 * ureg.amp) == 10 * ureg.ohm


def ΩVA(V, A):  # Ω=V/A
    return((V / A).to(ureg.ohm))


def test_ΩVA():
    assert ΩVA(10 * ureg.volt, 1 * ureg.amp) == 10 * ureg.ohm
