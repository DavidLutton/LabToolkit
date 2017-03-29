#!/usr/bin/env python3

import numpy as np
import pint
from pint import UnitRegistry
from pint.unit import UnitDefinition
from pint.converters import Converter


def decimalplace(x, y):
    # z = "{0:." + "{}".format(x) + "f~P}"
    return(("{0:." + "{}".format(x) + "f~P}").format(y))

dp = decimalplace


class Log10Converter(Converter):
    is_multiplicative = False

    def to_reference(self, value, inplace=False):
        return(-20 * np.log10((VSWR - 1) / (VSWR + 1)))

    def from_reference(self, value, inplace=False):
        return value

ureg = UnitRegistry()
Q_ = ureg.Quantity

ureg.default_format = '~P'
try:
    ureg.load_definitions('FrequencyRegistry.txt')
finally:
    pass
# except pint.errors.DefinitionSyntaxError:
#    pass

with ureg.context('rf'):
    Z = Q_(50, 'ohm')
    # print(Z.magnitude)
    # print(Z.units)
    print(Z)
    print()

    '''Q = Q_(27.5, 'cm')
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
    # print(Q_(230, 'MHz').to('cm'))

    print()
    # ** .5) == square root

    def WtoV(x):
        return(dp(8, (((Q_(x, 'watt') * Q_(50, 'ohm')) ** 0.5).to('volt'))))

    print(WtoV(6.48))
    print(WtoV(6.78))

    print("6.432W")
    q = (Z * Q_(6.432, 'watt')) ** 0.5
    print(q)
    print(q.to('V'))

    print()
    print("18V")
    q = Q_(18, 'volt') ** 2 / Z
    print(q)
    print(q.to('W'))

    '''print()
    q = (0 * ureg.dBm) + (0 * ureg.dBm)
    print(q)
    print(q.to('dBW'))
    print(q.to('dBk'))
    '''

    print()
    q = Q_(20, 'dBm')
    print(q)
    print(q.magnitude)
    res = (10 ** ((q - 30)/10)) * ureg.watt
    print(res)

    print()
    q = Q_(10, 'watt')
    print(q)
    print(q.magnitude)
    res = (10 * np.log10(q.magnitude / 0.001)) * ureg.dBm
    print(res)

    print()
    print("18V")
    q = (Q_(18, 'volt') ** 2 / Z).to('W')
    print(q)
    print(q.magnitude)
    res = (10 * np.log10(q.magnitude / 0.001)) * ureg.dBm
    print(res)

    print()
    q = 1 / Q_(5*60, 'seconds')
    print(q)
    print(dp(6, q.to('Hz')))
    print(dp(6, q.to('mHz')))

    print(Q_(1, 'pint').to('ml'))
