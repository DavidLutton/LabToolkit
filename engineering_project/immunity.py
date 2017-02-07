#!/usr/bin/env python3


def leveler(
    presentlevelatmeasurepoint,
    wantedlevelatmeasurepoint,
    presentlevelatgenerator,
):

    leveldelta = wantedlevelatmeasurepoint - presentlevelatmeasurepoint
    # print(leveldelta)

    levelnew = presentlevelatgenerator + leveldelta
    try:
        errorcent = (leveldelta / presentlevelatgenerator) * 100
    except ZeroDivisionError:
        errorcent = 0

    errorpwr = leveldelta
    return(errorpwr, errorcent, levelnew)
