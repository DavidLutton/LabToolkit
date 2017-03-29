#!/usr/bin/python
#
# This file is part of IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# IvPID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IvPID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#title           :test_pid.py
#description     :python pid controller test
#author          :Caner Durmusoglu
#date            :20151218
#version         :0.1
#notes           :
#python_version  :2.7
#dependencies    : matplotlib, numpy, scipy
#==============================================================================

import PID
import time
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.interpolate import spline

def test_pid(P=1,  I=20 , D=30.0):

    pid = PID.PID(P, I, D)

    pid.SetPoint=50
    #pid.setSampleTime(0.01)


    feedback = -10

    feedback_list = []
    setpoint_list = []

    for i in range(1,20):
        pid.update(feedback)
        output = pid.output
        print(output)
        feedback += (output - (1/i))
        time.sleep(0.02)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)


if __name__ == "__main__":
    test_pid(1.2, 1, 0.001)
#    test_pid(0.8, L=50)
