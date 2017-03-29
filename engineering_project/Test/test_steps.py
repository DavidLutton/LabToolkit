#!/usr/bin/env python3

import pytest

from steps import FrequencySweep


def test_FrequencySweep():
    sweep = FrequencySweep()
    sweep.setpoints([1100, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    sweep.step = sweep.stepper()
    assert(next(sweep.step) == 2)
    assert(next(sweep.step) == 3)
    assert(next(sweep.step) == 4)
    assert(next(sweep.step) == 5)
    assert(next(sweep.step) == 6)
    assert(next(sweep.step) == 7)
    assert(next(sweep.step) == 8)
    assert(next(sweep.step) == 9)
    assert(next(sweep.step) == 10)
    sweep.rewind = True
    assert(next(sweep.step) == 2)
    assert(next(sweep.step) == 3)
    assert(next(sweep.step) == 4)
    assert(next(sweep.step) == 5)
    assert(next(sweep.step) == 6)
    assert(next(sweep.step) == 7)
    assert(next(sweep.step) == 8)
    assert(next(sweep.step) == 9)
    assert(next(sweep.step) == 10)
    assert(next(sweep.step) == 11)
    assert(next(sweep.step) == 12)
    assert(next(sweep.step) == 13)
    assert(next(sweep.step) == 1100)

    with pytest.raises(StopIteration):
        next(sweep.step)
