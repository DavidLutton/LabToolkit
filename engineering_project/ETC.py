#!/usr/bin/env python3
import statistics


class ETC(object):
    """Estimated Time to Completion."""

    def __init__(self, numberofpoints):
        """Assume."""
        self.listoftimes = []
        self.points = numberofpoints + 1

    def append(self, timeinseconds, inferprogress=True):
        """Append result of timer."""
        # print(timeinseconds)
        self.listoftimes.append(timeinseconds)
        if inferprogress is True:
            self.points -= 1

    def ETC(self):
        """Estimate Time to Completion."""
        return("{0:.5f}".format((statistics.mean(self.listoftimes) * self.points)))
