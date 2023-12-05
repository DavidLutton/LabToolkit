"""Calculate various audio filters inc A-weighting filter."""

# from https://en.wikipedia.org/wiki/A-weighting#Function_realisation_of_some_common_weightings

import numpy as np


class IEC179Aweighting():
    def internal(self, f):
        return ( 12194**2 * f**4 ) / (
            (f**2 + 20.6**2) * 
            np.sqrt(
                (f**2 + 107.7**2) * (f**2 + 737.9**2)
            )
            * (f**2 + 12194**2)
        ) 
    
    def filter(self, f):
        return 20*np.log10(self.internal(f))- 20*np.log10(self.internal(1000))

class IEC179Bweighting():
    def internal(self, f):
        return ( 12194**2 * f**3 ) / (
            (f**2 + 20.6**2) * 
            np.sqrt(
                (f**2 + 158.2**2) 
            )
            * (f**2 + 12194**2)
        ) 
    
    def filter(self, f):
        return 20*np.log10(self.internal(f))- 20*np.log10(self.internal(1000))

class IEC179Cweighting():
    def internal(self, f):
        return ( 12194**2 * f**2 ) / (
            (f**2 + 20.6**2) * (f**2 + 12194**2)
        )
    
    def filter(self, f):
        return 20*np.log10(self.internal(f)) + 0.06


class ITU_R468noiseweighting():
    def filter(self, f):
        h1 = -4.737338981378384e-24 *  f**6 + 2.043828333606125e-15 * f**4 - 1.363894795463638e-7 * f**2 + 1
        h2 = 1.306612257412824e-19 * f**5 - 2.118150887518656e-11 * f**3 + 5.559488023498642e-4 * f
    
        R_ITU = 1.246332637532143e-4 * f / np.sqrt(h1**2 + h2**2)
        return 18.2 + 20 * np.log10(R_ITU)



# xa = np.linspace(20, 30e3, 2999)
# ya = IEC179Aweighting().filter(xa)