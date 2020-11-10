# print(f'Invoking __init__.py for {__name__}')

from .AgilentN9039A import AgilentN9039A



REGISTER = {
    'Agilent Technologies,N9039A': AgilentN9039A
}