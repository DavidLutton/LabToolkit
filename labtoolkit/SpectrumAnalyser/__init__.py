# print(f'Invoking __init__.py for {__name__}')


# from .AdvantestR3172 import AdvantestR3172
from .AgilentE4404B import AgilentE4404B
from .AgilentE4406A import AgilentE4406A
from .AgilentE4440A import AgilentE4440A
from .HP85nn import HP85nn
from .KeysightN9030B import KeysightN9030B

# from .KeysightN9010B import KeysightN9010B


REGISTER = {
    'Hewlett-Packard,E4406A': AgilentE4406A,
    'Hewlett-Packard,E4404B': AgilentE4404B,
    'Agilent Technologies,E4440A': AgilentE4440A,
    'Keysight Technologies,N9030B': KeysightN9030B,
#    'Keysight Technologies,N9010B': KeysightN9010B,

    'Hewlett-Packard,8563E,NO_IDN': HP85nn,
    'Hewlett-Packard,8563A,NO_IDN': HP85nn,
    # 'Advantest,R3172,NO_IDN_Recorded': AdvantestR3172,
}
