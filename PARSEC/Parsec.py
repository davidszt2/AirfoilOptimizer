"""PARSEC AIRFOIL PARAMETRIZATION"""
# Author: David Moeller Sztajnbok
# Date:   July 2023

import numpy as np
from math import tan, sqrt, pi

def createPMatrix(pArr):
    # pArr = [p1, p2, p3... p10, p11]
    # p1  - rLE Leading-edge radius
    # p2  - XS Upper crest position in horizontal coordinates
    # p3  - ZS Upper crest position in vertical coordinates
    # p4  - ZXX,S Upper crest curvature
    # p5  - XP Lower crest position in horizontal coordinates
    # p6  - ZP Lower crest position in vertical coordinates
    # p7  - ZXX,P Lower crest curvature
    # p8  - ZT E Trailing-edge offset
    # p9  - ∆ZT E Trailing-edge thickness
    # p10 - αT E Trailing-edge direction
    # p11 - βT E Trailing-edge wedge angle

    pMatrix = np.array(pArr)

    return pMatrix

"""TOP (SUCTION) SURFACE"""

def Csuction(pMatrix):
    p2 = pMatrix[1]

    Cs = np.array([
        np.ones(6),
        [p2**(1/2), p2**(3/2), p2**(5/2), p2**(7/2), p2**(9/2), p2**(11/2)],
        [1/2, 3/2, 5/2, 7/2, 9/2, 11/2],
        [(1/2)*(p2**(-1/2)), (3/2)*(p2**(1/2)), (5/2)*(p2**(3/2)), (7/2)*(p2**(5/2)), (9/2)*(p2**(7/2)), (11/2)*(p2**(11/2))],
        [(-1/4)*(p2**(-3/2)), (3/4)*(p2**(-1/2)), (15/4)*(p2**(1/2)), (35/4)*(p2**(3/2)), (63/4)*(p2**(5/2)), (99/4)*(p2**(7/2))],
        [1, 0, 0, 0, 0, 0]
    ])

    return Cs

def bsuction(pMatrix):
    p1 = pMatrix[0]
    p3 = pMatrix[2]
    p4 = pMatrix[3]
    p8 = pMatrix[7]
    p9 = pMatrix[8]
    p10 = pMatrix[9]
    p11 = pMatrix[10]

    bs = np.array([
        p8 + p9/2,
        p3,
        tan((p10 - p11/2) * pi/180),
        0,
        p4,
        sqrt(2*p1)
    ])

    return bs


"""BOTTOM (PRESSURE) SURFACE"""

def Cpressure(pMatrix):
    p5 = pMatrix[4]

    Cp = np.array([
        np.ones(6),
        [p5**(1/2), p5**(3/2), p5**(5/2), p5**(7/2), p5**(9/2), p5**(11/2)],
        [1/2, 3/2, 5/2, 7/2, 9/2, 11/2],
        [(1/2)*(p5**(-1/2)), (3/2)*(p5**(1/2)), (5/2)*(p5**(3/2)), (7/2)*(p5**(5/2)), (9/2)*(p5**(7/2)), (11/2)*(p5**(11/2))],
        [(-1/4)*(p5**(-3/2)), (3/4)*(p5**(-1/2)), (15/4)*(p5**(1/2)), (35/4)*(p5**(3/2)), (63/4)*(p5**(5/2)), (99/4)*(p5**(7/2))],
        [1, 0, 0, 0, 0, 0]
    ])

    return Cp

def bpressure(pMatrix):
    p1 = pMatrix[0]
    p6 = pMatrix[5]
    p7 = pMatrix[6]
    p8 = pMatrix[7]
    p9 = pMatrix[8]
    p10 = pMatrix[9]
    p11 = pMatrix[10]

    bp = np.array([
        p8 - p9/2,
        p6,
        tan((p10 + p11/2) * pi/180),
        0,
        p7,
        -sqrt(p1)
    ])

    return bp

"""POLYNOMIAL PARAMETER SOLUTIONS"""
def apress(pMatrix):
    Cp = Cpressure(pMatrix)
    bp = bpressure(pMatrix)

    apress = np.linalg.solve(Cp, bp)

    return apress

def asuct(pMatrix):
    Cs = Csuction(pMatrix)
    bs = bsuction(pMatrix)

    asuct = np.linalg.solve(Cs, bs)

    return asuct

"""CURVE GENERATION"""
def foilOrdinates(pMatrix, xArr=np.linspace(0, 1, 75)):
    asuction = asuct(pMatrix)
    apressure = apress(pMatrix)

    # Upper (suction) surface
    upperSurface = np.zeros_like(xArr)
    for i, coeff in enumerate(asuction):
        upperSurface += coeff * xArr**((i+1)/2)

    # Lower (pressure) surface
    lowerSurface = np.zeros_like(xArr)
    for i, coeff in enumerate(apressure):
        lowerSurface += coeff * xArr**((i+1)/2)

    # Adjust for x, y coordinates
    upperSurface = np.flip(upperSurface)

    yAirfoil = np.concatenate((upperSurface, lowerSurface))

    xTE = np.linspace(1, 0, len(upperSurface))
    xLE = np.linspace(0, 1, len(lowerSurface))
    xAirfoil = np.concatenate((xTE, xLE))

    return xAirfoil, yAirfoil
