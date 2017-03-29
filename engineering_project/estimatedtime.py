#!/usr/bin/env python3
import statistics


class estimatedtime:
    def __init__(self, numberofpoints):
        self.listoftimes = []
        self.points = numberofpoints

    def append(self, timeinseconds, inferprogress=True):
        # print(timeinseconds)
        self.listoftimes.append(timeinseconds)
        if inferprogress is True:
            self.points -= 1

    def ETA(self):
        return("{0:.5f}".format((statistics.mean(self.listoftimes) * self.points)))
