import time


def level(wantedlevel = -10,  presentlevel= -9.96, genlevel = -2.9):
    leveldelta = wantedlevel - presentlevel
    
    suggestedgenlevel = genlevel + (leveldelta * .92)
    return {
        'delta': round(leveldelta, 2),
        'source': round(suggestedgenlevel, 2),
    }
    
    
    
def alc(target, settingaccuracy, source, meas, settlingtime):
    """."""
    state = target, meas.amplitude, source.amplitude

    while abs(level(*state )['delta']) > settingaccuracy:
        # print()

        # print(state, level(*state)['delta'], level(*state)['source'])
        '''
        if level(*state)['delta'] > 3:
            gen.amplitude = gen.amplitude + 2
        elif level(*state)['delta'] < 3:
            gen.amplitude = gen.amplitude - 2
        '''
        if abs(level(*state )['delta']) > settingaccuracy:
            source.amplitude = level(*state)['source']

        time.sleep(settlingtime)
        state = target, meas.amplitude, source.amplitude

        # print(state, level(*state)['delta'], level(*state)['source'])
    return True


# alc(-11, 0.4, gen, an, .6)



class AmplitudeLimiter(object):
    """."""

    def __init__(self, f, *args, **kwargs):
        """If thereareno decorator args the function tobe decorated is passed to the constructor."""
        # print(f)
        # print(*args)
        # print(**kwargs)
        # print("Inside __init__()")

        self.f = f

    def __call__(self, f, *args, **kwargs):
        """The __call__ method is not called until the decorated function is called."""
        # print(f)
        print(*args)
        # print(**kwargs)
        # print("Inside __call__()")
        setpoint = float(*args)
        if setpoint >= f.amplimit:
            f.log.warn(
                "Amplimit ({}) reached with setpoint ({}) on {}"
                .format(f.amplimit, setpoint, f.instrument))
        else:
            self.f(f, *args)
        # print("After self.f(*args)")

        