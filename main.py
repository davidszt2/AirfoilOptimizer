"""AIRFOIL OPTIMIZATION"""
# Author: David Moeller Sztajnbok
# Date:   July 2023

from PARSEC.Parsec import createPMatrix, foilOrdinates
from BEZIER.Bezier import BEZIERfoil, plotBEZIER
from Airfoil import runAirfoil, createPolarDict
import numpy as np
import matplotlib.pyplot as plt

"""PARSEC EXAMPLE"""
pArr = [
    0.0130,     # p1  - rLE Leading-edge radius
    0.2876,     # p2  - XS Upper crest position in horizontal coordinates
    0.0566,     # p3  - ZS Upper crest position in vertical coordinates
    -0.3951,    # p4  - ZXX,S Upper crest curvature
    0.2127,     # p5  - XP Lower crest position in horizontal coordinates
    -0.0290,    # p6  - ZP Lower crest position in vertical coordinates
    0.2602,     # p7  - ZXX,P Lower crest curvature
    0,          # p8  - ZT E Trailing-edge offset
    0,          # p9  - ∆ZT E Trailing-edge thickness
    -1.7939,    # p10 - αT E Trailing-edge direction
    3.5879      # p11 - βT E Trailing-edge wedge angle
    ]

pMatrix = createPMatrix(pArr)
X, Y = foilOrdinates(pMatrix)

plt.plot(X, Y)
plt.xlabel('x')
plt.ylabel('y')
plt.title("PARSEC Airfoil")
plt.gca().set_aspect('equal')
plt.show()

# try:
#     polar = runAirfoil(X, Y, "otherTest", 1e6, np.linspace(-5, 15, 21))
# except Exception as ex:
#     print(ex)
#
# foilPolar = createPolarDict(polar, "otherTest")

"""BEZIER EXAMPLE"""

controlPoints = [
    [1, 0.001],         # trailing edge (top)
    [0.76, 0.08],
    [0.52, 0.125],
    [0.25, 0.12],
    [0.1, 0.08],
    [0, 0.03],          # leading edge (top)
    [0, -0.03],         # leading edge (bottom)
    [0.15, -0.08],
    [0.37, -0.01],
    [0.69, 0.04],
    [1, -0.001]         # trailing edge (bottom)
]

X, Y = BEZIERfoil(controlPoints, 16)
plotBEZIER(X, Y, controlPoints)

plt.show()
