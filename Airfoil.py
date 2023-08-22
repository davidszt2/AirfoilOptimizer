"""AIRFOIL CREATION TOOLS"""
# Author: David Moeller Sztajnbok
# Date:   July 2023

from xfoil import polar
import numpy as np


def createDATFile(X, Y, name):
    fileName = f"{name}.dat"
    fid = open(fileName, "w")

    print(name, file=fid)
    for i in range(len(X)):
        print(f"{X[i].round(5)}     {Y[i].round(5)}", file=fid)

    fid.close()

    return


def runAirfoil(X, Y, name, Re, iterList, iterative='alpha'):
    # X, Y      : foil coordinates
    # name      : name for .dat file
    # Re        : Reynold's number
    # iterList  : list of iterative parameters (AoA or CL depending on iterative parameter)
    # iterative : 'alpha' if iterList are AoAs or 'cl' if iterList are CLs

    createDATFile(X, Y, name)

    if iterative == 'alpha':
        foilPolar = polar(f"{name}.dat", Re, alfaseq=iterList)
    elif iterative == 'cl':
        foilPolar = polar(f"{name}.dat", Re, clseq=iterList)

    return foilPolar


def createPolarDict(polar, name, type):

    # type - cl or alpha depending on whether iterating through cl or alpha

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

    # print(polar)

    alpha = polar['a'].copy()
    cl = polar['cl'].copy()
    cd = polar['cd'].copy()

    if type == "alpha":
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
        foilPolar['ldmax'] = np.nanmax(foilPolar['ld'])
        foilPolar['cdmin'] = np.nanmin(foilPolar['cd'])

        ldmaxIdx = foilPolar['ld'].index(foilPolar['ldmax'])
        cdminIdx = foilPolar['cd'].index(foilPolar['cdmin'])

        foilPolar['ldmaxloc'] = foilPolar['cl'][ldmaxIdx]
        foilPolar['cdminloc'] = foilPolar['cl'][cdminIdx]

    elif type == "cl":
        foilPolar['alpha'] = list(alpha)
        foilPolar['cl'] = list(cl)
        foilPolar['cd'] = list(cd)

        # Derived parameters
        foilPolar['ld'] = list(np.array(cl)/np.array(cd))
        # foilPolar['ldmax'] = np.nanmax(foilPolar['ld'])
        # foilPolar['cdmin'] = np.nanmin(foilPolar['cd'])

        # ldmaxIdx = foilPolar['ld'].index(foilPolar['ldmax'])
        # cdminIdx = foilPolar['cd'].index(foilPolar['cdmin'])
        #
        # foilPolar['ldmaxloc'] = foilPolar['cl'][ldmaxIdx]
        # foilPolar['cdminloc'] = foilPolar['cl'][cdminIdx]

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
