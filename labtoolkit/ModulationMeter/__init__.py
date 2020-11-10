# print(f'Invoking __init__.py for {__name__}')

from .HP8901B import HP8901B
from .MI2305 import MI2305

REGISTER = {
    'HEWLETT-PACKARD,8901B,NO_IDN': HP8901B,
    'Marconi Instuments,2305': MI2305,
}
