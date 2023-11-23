"""AIRFOIL CREATION TOOLS"""
# Author: David Moeller Sztajnbok
# Date:   July 2023

from xfoil_alt import singleAlpha, alphaRange, singleCL, CLRange
import numpy as np


def createDATFile(X, Y, name):
    fileName = f"{name}.dat"
    fid = open(fileName, "w")

    print(name, file=fid)
    for i in range(len(X)):
        print(f"{X[i].round(5)}     {Y[i].round(5)}", file=fid)

    fid.close()

    return


def runAirfoil(X, Y, name, Re, iterStart, iterEnd, iterStep, iterative='alpha'):
    # X, Y      : foil coordinates
    # name      : name for .dat file
    # Re        : Reynold's number
    # iterList  : list of iterative parameters (AoA or CL depending on iterative parameter)
    # iterative : 'alpha' if iterList are AoAs or 'cl' if iterList are CLs

    createDATFile(X, Y, name)

    if iterative == 'alpha':
        foilPolar = alphaRange(f"{name}.dat", Re, iterStart, iterEnd, iterStep)
    elif iterative == 'cl':
        foilPolar = CLRange(f"{name}.dat", Re, iterStart, iterEnd, iterStep)

    return foilPolar
