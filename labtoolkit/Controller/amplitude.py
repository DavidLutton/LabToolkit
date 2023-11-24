from time import sleep


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
       
        if abs(level(*state )['delta']) > settingaccuracy:
            source.amplitude = level(*state)['source']

        sleep(settlingtime)
        state = target, meas.amplitude, source.amplitude

        # print(state, level(*state)['delta'], level(*state)['source'])
    return state