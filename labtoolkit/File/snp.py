
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
    

