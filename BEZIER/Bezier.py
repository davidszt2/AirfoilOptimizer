"""BEZIER AIRFOIL PARAMETRIZATION"""
# Author:   N. Rooy, August 2015
# Modified: David Moeller Sztajnbok, July 2023

import matplotlib.pyplot as plt
import numpy as np

def quadraticBezier(t, points):
    B_x = (1 - t) * ((1 - t) * points[0][0] + t * points[1][0]) + t * ((1 - t) * points[1][0] + t * points[2][0])
    B_y = (1 - t) * ((1 - t) * points[0][1] + t * points[1][1]) + t * ((1 - t) * points[1][1] + t * points[2][1])
    return B_x, B_y


def BEZIERfoil(controlPoints, numPoints):
    curve = []
    t = np.array([i / numPoints for i in range(0, numPoints)])

    # First points
    midX = (controlPoints[1][0] + controlPoints[2][0]) / 2
    midY = (controlPoints[1][1] + controlPoints[2][1]) / 2
    B_x, B_y = quadraticBezier(t, [controlPoints[0], controlPoints[1], [midX, midY]])
    curve = curve + list(zip(B_x, B_y))

    # Middle Points
    for i in range(1, len(controlPoints) - 3):
        p0 = controlPoints[i]
        p1 = controlPoints[i + 1]
        p2 = controlPoints[i + 2]
        midX_1 = (p0[0] + p1[0]) / 2
        midY_1 = (p0[1] + p1[1]) / 2
        midX_2 = (p1[0] + p2[0]) / 2
        midY_2 = (p1[1] + p2[1]) / 2

        B_x, B_y = quadraticBezier(t, [[midX_1, midY_1], p1, [midX_2, midY_2]])
        curve = curve + list(zip(B_x, B_y))

    # Last points
    midX = (controlPoints[-3][0] + controlPoints[-2][0]) / 2
    midY = (controlPoints[-3][1] + controlPoints[-2][1]) / 2

    B_x, B_y = quadraticBezier(t, [[midX, midY], controlPoints[-2], controlPoints[-1]])
    curve = curve + list(zip(B_x, B_y))
    curve.append(controlPoints[-1])

    xAirfoil, yAirfoil = zip(*curve)

    return xAirfoil, yAirfoil


def plotBEZIER(X, Y, controlPoints):
    xControl, yControl = zip(*controlPoints)

    # Airfoil
    plt.plot(X, Y, 'b')

    # Control points
    plt.plot(xControl, yControl, color='#666666', marker='o', mec='r', linestyle='--')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.gca().set_aspect('equal')

    return
