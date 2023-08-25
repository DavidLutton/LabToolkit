from numpy import sqrt, log10, pi, arctan2  # arccosh, conj
# Prefer numpy over math as handling list/arrays of values works in numpy
# Produces same result for single values

import scipy.constants as constants
# https://docs.scipy.org/doc/scipy/reference/constants.html


class VoltTo():

    @staticmethod
    def amp(volt):
        Z = 50
        return volt / Z

    @staticmethod
    def watts(volt):
        Z = 50
        return volt**2 / Z

    @staticmethod
    def dBm(volt):
        """Volt to dBm."""
        return 20 * log10(volt) + 13
        # return WattsTo.dBm(voltTo.watts(volt))

    @staticmethod
    def dBuA(volt):
        """Volt to dBuA."""
        return 20 * log10(volt) + 86

    @staticmethod
    def dBuV(volt):
        return 20 * log10(volt) + 120  # checked against R&S unit converter

    @staticmethod
    def dBV(volt):
        return 20 * log10(volt)

    @staticmethod
    def watt(volt):
        Z = 50
        return volt ** 2 / Z


class dBmTo():

    @staticmethod
    def watt(dBm):
        """.

        :param dBm: dBm
        :returns: Watts
        """
        return 10 ** ((dBm - 30) / 10)

    @staticmethod
    def milliwatt(dBm):
        """.

        :param dBm: dBm
        :returns: Milliwatts
        """
        return 10 ** (dBm / 10)

    @staticmethod
    def dBuV(dBm):
        """μ."""
        Z = 50
        return dBm + 10 * log10(Z) + 90

    @staticmethod
    def dBuA(dBm):  # , *, Z=50):
        Z = 50
        return dBm - 10 * log10(Z) + 90

    @staticmethod
    def volt(dBm):  # , *, Z=50):
        # Z = 50
        return 10 ** ((dBm - 13) / 20)

    @staticmethod
    def amp(dBm):
        return 10 ** ((dBm - 47) / 20)


class MilliwattTo:

    @staticmethod
    def dBm(milliwatt):
        """milliwatt to dBm.

        :param watt: Watt
        :returns: dBm
        """
        # return 10 * log10((watt / 0.001))
        return 10 * log10(milliwatt)


class WattTo:

    @staticmethod
    def volt(watt):
        """Watts to volt."""
        Z = 50  # Nominal 50 Ohms
        # watt = 6.5
        return sqrt(watt * Z)
        # >>> 18.027756377319946

    @staticmethod
    def amp(watt):
        Z = 50  # Nominal 50 Ohms
        return sqrt(watt / Z)

    @staticmethod
    def dBm(watt):
        """Watts to dBm.

        :param watt: Watt
        :returns: dBm
        """
        # return 10 * log10((watt / 0.001))
        return 10 * log10(watt) + 30

    @staticmethod
    def dBW(watt):
        """Watts to dBW.
        
        :param watt: Watt
        :returns: dBW
        """
        return 10 * log10(watt)

    @staticmethod
    def dBuV(watt):
        return 10 * log10(watt) + 137

    @staticmethod
    def dBuA(watt):
        return 10 * log10(watt) + 103


class OhmsTo:

    @staticmethod
    def dBOhm(ohm):
        return 20 * log10(ohm)


class dBOhmsTo:

    @staticmethod
    def Ohm(dBOhm):
        return 10 ** (dBOhm / 20)


class dBuVTo:

    @staticmethod
    def watt(dBuV):
        # Z = 50
        return 10 ** ((dBuV - 137) / 10)

    @staticmethod
    def amp(dBuV):
        # Z = 50
        return 10 ** ((dBuV - 154) / 20)

    @staticmethod
    def dBm(dBuV):
        Z = 50
        # return dBuV - 90 + 10*log10(Z)
        return dBuV - 10 * log10(Z) - 90

    @staticmethod
    def dBuA(dBuV):
        Z = 50
        # return dBuV - log20(Z)
        return dBuV - 20 * log10(Z)

    @staticmethod
    def volt(dBuV):
        return 10**((dBuV - 120) / 20)  # checked against R&S unit converter

    @staticmethod
    def dBV(dBuV):
        return dBuV - 120


class dBVTo:

    @staticmethod
    def dBuV(dBV):
        return dBV + 120

    @staticmethod
    def volt(dBV):
        return 10 ** (dBV / 20)


class dBuATo:

    @staticmethod
    def dBuV(dBuA):
        Z = 50
        # return dBuA + log20(Z)
        return dBuA + 20 * log10(Z)

    @staticmethod
    def dBm(dBuA):
        Z = 50
        return dBuA + 10 * log10(Z) - 90

    @staticmethod
    def amp(dBuA):
        return 10 ** ((dBuA - 120) / 20)

    # uA = 10**(dBuA / 20)

    @staticmethod
    def volt(dBuA):
        return 10 ** ((dBuA - 86) / 20)

    @staticmethod
    def watt(dBuA):
        return 10 ** ((dBuA - 103) / 10)

    @staticmethod
    def dBA(dBuA):
        return dBuA - 120


class dBATo:

    @staticmethod
    def dBuA(dBA):
        return dBA + 120


class AmpTo:

    @staticmethod
    def volt(amp):
        Z = 50
        return amp * Z

    @staticmethod
    def watt(amp):
        Z = 50
        return amp**2 * Z

    @staticmethod
    def dBuA(amp):
        return 20 * log10(amp) + 120

    @staticmethod
    def dBm(amp):
        return 20 * log10(amp) + 47

    @staticmethod
    def dBuV(amp):
        return 20 * log10(amp) + 154

    @staticmethod
    def dBA(amp):
        return 20 * log10(amp)

    # 20 * log10(uA)


class uTTo:

    @staticmethod
    def A_m(uT):
        return uT / 1.25


def impedance_of_free_space():
    c = constants.speed_of_light  # Speed of Light
    h = constants.h  # Planck constant
    e = constants.elementary_charge  # elementary_charge
    R_inf = constants.Rydberg  # Rydberg constant
    m_e = constants.electron_mass  # electron mass

    α = sqrt(2 * h * R_inf / (m_e * c))
    # = α = alpha = fine_structure_constant

    vacuum_permeability = 2 * α * h / (e ** 2 * c)
    # = µ_0 = mu_0 = mu0 = magnetic_constant

    vacuum_permittivity = e ** 2 / (2 * α * h * c)
    # = ε_0 = epsilon_0 = eps_0 = eps0 = electric_constant

    impedance_of_free_space = sqrt(
        vacuum_permeability / vacuum_permittivity
        )
    # impedance_of_free_space = 2 * α * h / e ** 2
    # = Z_0 = characteristic_impedance_of_vacuum

    return round(impedance_of_free_space, 9)
    # uncertainty beyond 9 decimal places, according to NIST publication
