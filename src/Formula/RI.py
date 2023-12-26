import numpy as np


def complexto(c=0.0025+0.005j, *, Z0=50, reflective=False):  # c is a complex number or array of complex numbers
    """."""
    
    R = (1-c.real**2-c.imag**2)/((1-c.real)**2+c.imag**2)*Z0  # R real impedance
    X = 2*c.imag/((1-c.real)**2+c.imag**2)*Z0  # X imag impedance
    Z = np.sqrt(X**2+R**2)  # ZO, Impedance

    magnitude = np.abs(c)
    
    dB = 20 * np.log10(magnitude)
    
    # dB = 10 * np.log10((reim.real**2 + reim.imag**2))  🔻
    # Disagrees with HP 4395A for small values -1.909  (dB -0.053) from -0.8002815+0.06101832j
    
    # quadrature = (npy.abs(c), npy.angle(c)*npy.abs(c))

    # Γ
    # ρ=abs(Γ)
    calcs = {
        'R': R,
        'X': X,
        'impedance': Z,

        # 'dB': 20 * np.log10(np.sqrt(c.real**2 + c.imag**2)),
        'dB': 20 * np.log10(magnitude),
        # 'VSWR': (1 + np.sqrt(c.real**2+c.imag**2)) / (1 - np.sqrt(c.real**2+c.imag**2)), 
        'VSWR': (1 + magnitude) / (1 - magnitude), 

        'magnitude': np.abs(c),
        # 'radians': np.angle(c),  # radians by default
        
        # 'phase': np.degrees(np.arctan(X/R)),  # phase in degrees  ?????????????? TODO
        'phase': np.angle(np.arctan(c), deg=True),
        # np.degrees(np.arctan(resp['X']/resp['R']))


        'real': np.real(c), 
        'imag': np.imag(c), 
        
        
        # https://www.microwaves101.com/encyclopedias/mismatch-loss-etc
        # https://en.wikipedia.org/wiki/Mismatch_loss
    }
    if reflective == True:
        pass
        # 'MLdB': -10 * np.log10(1- (10**(dB)/20))**2  # Only valid for reflective port

    '''if isinstance(c, np.ndarray) and len(c) > 1:
        unwrap_phase = (np.unwrap(calcs['radians'], axis=0))*180/np.pi  # Unwrap phase
        return {**calcs, **{'unwrap_phase': unwrap_phase}}
    else:
        return calcs'''
    return calcs
    # groupdelay, phase from delay, Inductance, capactance, series quality factor, parallel quality factor



'''

# magnitude, angle = 0.298055, -57.407345
# re = magnitude * np.cos(np.deg2rad(angle))
# im = magnitude * np.sin(np.deg2rad(angle))
# c = complex(re, im)
# from reimtoZPhase.py
import math

re, im = -0.829801, 0.0609607

R = (1-re**2-im**2)/((1-re)**2+im**2)*50
X = 2*im/((1-re)**2+im**2)*50

Z = (R**2+X**2) ** 0.5
PHASE = math.degrees(math.atan(X/R))

assert Z == 4.937330973284211
assert PHASE == 21.614287755407542

re = -0.03634939
im = 0.0915885
# assert Z == 46.520753285555344
# assert PHASE = 10.479724479279204

# print(Z)
# print(PHASE)


re, im = 0.293816656, -0.200716108  # RL -8.98  VSWR 2.10

# print(20*math.log10((re**2+im**2)**0.5))  # RL
RL = 20*math.log10((re**2+im**2)**0.5)

# RL = -8.98
# RLtoVSWR
# print(-(1+10**(-RL/20))/(1-10**(-RL/20)))


re, im = 0.4481426, -0.06830621
R = (1-re**2-im**2)/((1-re)**2+im**2)*50
X = 2*im/((1-re)**2+im**2)*50

Z = (R**2+X**2) ** 0.5
PHASE = math.degrees(math.atan(X/R))


print(R)
print(X)
print(Z)

'''
'''
if __name__ == '__main__':
    magnitude, angle = 0.298055, -57.407345
    re = magnitude * np.cos(np.deg2rad(angle))
    im = magnitude * np.sin(np.deg2rad(angle))
    # complexto(np.array([1.+2.j, 3.+4.j, 5.+6.j]))
    from pprint import pprint
    # pprint(complexto(complex(re, im)))
    # pprint(complexto(complex(1, 1)))
    # pprint(complexto(complex(-0.829801, 0.0609607)))
    pprint(complexto(complex(0.293816656, -0.200716108)))
    # -0.03634939 im = 0.0915885
'''