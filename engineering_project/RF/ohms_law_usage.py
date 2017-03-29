#!/usr/bin/env python3

from pint import UnitRegistry

import ohms_law as OLT  # Ohms Law traditional
# IPR, IPV, IVR, PIR, PVI, PVR, RPI, RVI, RVP, VIR, VPI, VPR
# AVΩ, AWV, AWΩ, WAΩ, WVA, WVΩ, ΩWA, ΩVA, ΩVW, VAΩ, VWA, VWΩ
import ohms_law_SI as OLS  # Ohms Law Standard

ureg = UnitRegistry()


ret = OLT.RVI(48 * ureg.volt, 0.96 * ureg.amp)
print(ret)
print(str(ret.magnitude) + " " + str(ret.units))

print(OLT.VPR(50 * ureg.ohm, 6.432 * ureg.watt))  # 17.933209417167912 volt
print(OLT.PVR(18 * ureg.volt, 50 * ureg.ohm))  # 6.48 watt
