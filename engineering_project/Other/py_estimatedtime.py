import statistics as stat


def estimatedtimeremaining(listoffloatsinseconds, ticksremaining):
    # Estimate  time to test  completion  given  the  mean of times  per  tick mutiplied  by the  ticks  remaining
    return(stat.mean(listoffloatsinseconds) * ticksremaining)


def estimatedtimeremainingmins(listoffloatsinseconds, ticksremaining):
    return "{0:.2f}".format(estimatedtimeremaining(listoffloatsinseconds, ticksremaining) / 60)

ticktimes = [1.2, 1.3, 1.4]
print(estimatedtimeremaining(ticktimes, 64))
# 83.2
