# print(f'Invoking __init__.py for {__name__}')

from .Racal1992 import *
from .HP53132A import *


REGISTER = {
    'HEWLETT-PACKARD,53132A': HP53132A,
    'Racal,1992,NO_IDN': Racal1992,
}
