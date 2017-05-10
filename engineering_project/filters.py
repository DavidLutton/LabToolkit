#!/usr/bin/env python3
import statistics
import time

'''
class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
'''


def stdevlowpass(*, tolerance=0.05, delay=0.1, readings=10, instrument=False, abortafter=42):
    """Standard deviation low pass filter.

    :param tolerance: tolerace upper limit required to pass
    :param delay: delay between readings
    :param readings: readings to take before applying filter
    :param instrument: Instrument that has a measurement function
    :param abortafter: the upper limit before bypassing this filter
    :returns: list of values as made by readback
    """
    try:
        run = 0
        meas = []
        measurethreshold = False
        while measurethreshold is not True:
            run += 1
            if run >= abortafter:
                raise Exception("Abort limit reached: {}".format(abortafter))

            meas.append(instrument.measurement)
            # print(meas)
            if len(meas) > readings:
                meas.pop(0)  # remove item at index 0
                stddev = statistics.stdev(meas)
                # print(stddev)
                if stddev < tolerance:
                    measurethreshold = True
            time.sleep(delay)
    finally:
        return(meas)
