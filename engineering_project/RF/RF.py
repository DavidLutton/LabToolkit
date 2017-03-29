#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np


def VSWR2RL(VSWR):
    return(-20 * np.log10((VSWR - 1) / (VSWR + 1)))


def RL2VSWR(RL):
    return((10 ** (RL / 20) + 1) / (10 ** (RL / 20) - 1))


def test_RL2VSWR():
    assert RL2VSWR(30) == 1.0653108640674351
    assert RL2VSWR(60) == 1.002002002002002
    assert RL2VSWR(0.5) == 34.75315212699187


def test_VSWR2RL():
    assert VSWR2RL(1.2) == 20.827853703164504
    assert VSWR2RL(1.002) == 60.00868154958637
    assert VSWR2RL(100) == 0.17372358370185334


def VSWR2Refl(VSWR):  # ectionCoefficient
    return((VSWR - 1)/(VSWR + 1))


def test_VSWR2Refl():
    assert VSWR2Refl(1.50) == 0.2


'''
 Γ=10(‐ReturnLoss/20)
 VSWR=(1+|Γ|)/(1‐|Γ|)
 MismatchLoss(dB)=10log(Γ**2)
 ReflectedPower(%)=100*Γ **2
 ReturnLoss(dB)= ‐20log|Γ|
 Γ=(VSWR‐1)/(VSWR+1)
 ThroughPower(%)=100(1‐Γ2)
'''
