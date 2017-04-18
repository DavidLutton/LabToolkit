#!/usr/bin/env python3

# import matplotlib.pyplot as plt
from pprint import pprint
from scipy.interpolate import UnivariateSpline
import numpy as np

x = [100e3, 300e3, 1e6, 3e6, 10e6, 30e6, 50e6, 100e6, 300e6, 1000e6, 2000e6, 3000e6, 4200e6]
y = [95.1, 97.6, 99.2, 98.8, 98.4, 98.2, 98, 98, 97.9, 97.5, 96.6, 95.1, 90.4]
assert len(x) == len(y)
# zipped = dict(zip(x, y))
print(x)
print(y)

xi = [100e3, 200e3, 300e3, 500e3, 3333e6, 1e6, 3e6, 10e6, 30e6, 50e6, 100e6, 300e6, 400e6,
      500e6, 600e6, 700e6, 800e6, 900e6, 1000e6, 1100e6, 1200e6, 1300e6, 1400e6,
      1500e6, 1600e6, 1700e6, 1800e6, 1900e6, 2000e6, 2100e6, 2200e6, 2300e6,
      2400e6, 2500e6, 2600e6, 2700e6, 2800e6, 2900e6, 3000e6, 3100e6, 3200e6,
      3300e6, 3400e6, 3500e6, 3600e6, 3700e6, 3800e6, 3900e6, 4000e6, 4100e6, 4200e6]

# xi = []

# z = np.arange(100e6, 4200e6, 50e6)
# xi = [3333.333e6, 2222.222e6, 1111.111e6]

for each in x:
    xi.append(each)
xi.sort()

# y1 = UnivariateSpline(x, y, k=5, s=.05)
# res = y1(xi)
res = (UnivariateSpline(x, y, k=5, s=.05))(xi)

dictonaryoffactor = {}
for idx, val in enumerate(xi):
    dictonaryoffactor[xi[idx]] = float("{0:.2f}".format(res[idx]))

pprint(dictonaryoffactor)

'''plt.figure()
#plt.plot(x, y, 'x', xi, y1, 'b')
plt.plot(x, y, 'b', xi, res, 'o')
plt.legend(['Data', 'Interpolate'])
#plt.axis([-0.05, 6.33, -1.05, 1.05])
plt.title('UnivariateSpline')
plt.show()
'''
