
import numpy as np
import datetime


def save_S1P(dest, x, y, *, Z0=50):
    data = np.column_stack((x, y.real, y.imag))
    # print(data)
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    # timestamp = f'ISO8601 Date: {now}'
    np.savetxt(
        dest, 
        data, 
        fmt='%i %9.8f %9.8f', 
        header='! '+'\n! '.join(['Created by Python, David', 'Trace details', 'Frequency S-Parameter(RI)'])+'\n# HZ S RI R 50', 
        comments=''
    )
    
def save_S2P(dest, x, y1, y2, y3, y4, *, Z0=50):
    data = np.column_stack((x, y1.real, y1.imag, y2.real, y2.imag, y3.real, y3.imag, y4.real, y4.imag))
    # print(data)
    np.savetxt(
        dest, 
        data, 
        fmt='%i %9.8f %9.8f %9.8f %9.8f %9.8f %9.8f %9.8f %9.8f',
        header='! '+'\n! '.join(['Created by Python, David', 'Trace details', 'Frequency S-Parameter(RI)'])+'\n# HZ S RI R 50', 
        comments=''
    )

    
def read_S2P(s2pfile, *, Z0=50):
    arr = np.loadtxt(s2pfile, comments=['!', '#'])
    # arr.shape
    x = arr[:, [0]].flatten()
    y = {}
    y['S11'] = arr[:, [1, 2]].flatten().view(np.complex128)
    y['S12'] = arr[:, [3, 4]].flatten().view(np.complex128)
    y['S21'] = arr[:, [5, 6]].flatten().view(np.complex128)
    y['S22'] = arr[:, [7, 8]].flatten().view(np.complex128)
    return x, y['S11'], y['S12'], y['S21'], y['S22']    
    


def complexto(c=0.0025+0.005j, *, Z0=50, reflective=False):  # c is a complex number or array of complex numbers
    """."""
    
    R = (1-c.real**2-c.imag**2)/((1-c.real)**2+c.imag**2)*Z0  # R real impedance
    X = 2*c.imag/((1-c.real)**2+c.imag**2)*Z0  # X imag impedance 
    Z = np.sqrt(X**2+R**2)  # ZO, Impedance

    magnitude = np.abs(c)
    
    dB = 20 * np.log10(magnitude)
    # quadrature = (npy.abs(c), npy.angle(c)*npy.abs(c))
    # dBfrommag = 20 * np.log10(magnitude)  # PASS~ 0 sliver of 0
    # print(dBfrommag)
    # dB - dBfrommag ~0    
    
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
