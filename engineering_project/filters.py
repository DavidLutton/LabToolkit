#!/usr/bin/env python3
import statistics


def stdevlowpass(stddevtolerance=0.05, delay=0.1, readings=10, readback=0):
    """Standard deviation low pass filter."""
    try:
        measure = False
        meas = []

        while measurethreshold is not True:
            meas.append(readback)
            # print(meas)
            if len(meas) > readings:
                meas.pop(0)  # remove item at index 0
                stddev = statistics.stdev(meas)
                # print(stddev)
                if stddev < stddevtolerance:
                    measurethreshold = True
            time.sleep(delay)
    finally:
        return(meas)
