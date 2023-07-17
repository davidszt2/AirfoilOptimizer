"""AIRFOIL CREATION TOOLS"""
# Author: David Moeller Sztajnbok
# Date:   July 2023

from xfoil import polar
import numpy as np
import os


def createDATFile(X, Y, name):
    fileName = f"{name}.dat"
    fid = open(fileName, "w")

    print(name, file=fid)
    for i in range(len(X)):
        print(f"{X[i].round(5)}     {Y[i].round(5)}", file=fid)

    fid.close()

    return


def runAirfoil(X, Y, name, Re, alphaList):
    createDATFile(X, Y, name)

    foilPolar = polar(f"{name}.dat", Re, alphaList)
    os.remove(f"./{name}.dat")

    return foilPolar


def createPolarDict(polar, name):
    foilPolar = {
        'name': name,   # Airfoil Name (identifier)
        'alpha': [],    # Angle of Attack Array
        'cl': [],       # Coefficient of Lift Array
        'cd': [],       # Coefficient of Drag Array
        'ld': [],       # Lift-to-Drag Ratio Array (cl/cd)
        'ldmax': 0,     # Maximum Lift-to-Drag Ratio
        'cdmin': 0,     # Minimum Coefficient of Drag
        'ldmaxloc': 0,  # Location of LDmax (Cl at which it occurs)
        'cdminloc': 0   # Location of Cdmin (Cl at which it occurs)
    }

    alpha = polar['a'].copy()
    cl = polar['cl'].copy()
    cd = polar['cd'].copy()

    completeAlpha = set(range(-5, 16))
    missingAlpha = completeAlpha - set(alpha)

    newAlpha = np.concatenate((alpha, list(missingAlpha)))
    newCl = np.concatenate((cl, [np.nan] * len(missingAlpha)))
    newCd = np.concatenate((cd, [np.nan] * len(missingAlpha)))

    sortedLists = sorted(zip(newAlpha, newCl, newCd), key=lambda x: x[0])
    sortedAlpha, sortedCl, sortedCd = zip(*sortedLists)

    sortedAlpha = list(sortedAlpha)
    sortedCl = list(sortedCl)
    sortedCd = list(sortedCd)

    foilPolar['alpha'] = sortedAlpha
    foilPolar['cl'] = sortedCl
    foilPolar['cd'] = sortedCd

    # Derived parameters
    foilPolar['ld'] = list(np.array(sortedCl)/np.array(sortedCd))
    foilPolar['ldmax'] = max(foilPolar['ld'])
    foilPolar['cdmin'] = min(foilPolar['cd'])

    ldmaxIdx = foilPolar['ld'].index(foilPolar['ldmax'])
    cdminIdx = foilPolar['cd'].index(foilPolar['cdmin'])

    foilPolar['ldmaxloc'] = foilPolar['cl'][ldmaxIdx]
    foilPolar['cdminloc'] = foilPolar['cl'][cdminIdx]

    return foilPolar


def getCLmax(polar):
    return max(polar['cl'])


def getLDmax(polar):
    return max(polar['ld'])


def getCDmin(polar):
    return min(polar['cd'])


def getLDmaxLOC(polar):
    return polar['ldmaxloc']


def getCDminLOC(polar):
    return polar['cdminloc']
