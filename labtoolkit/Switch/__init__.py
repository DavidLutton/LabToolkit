# print(f'Invoking __init__.py for {__name__}')


from .HP3488A import HP3488A


REGISTER = {
    'HEWLETT-PACKARD,3488A,NO_IDN': HP3488A,
}
