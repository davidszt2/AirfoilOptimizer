"""AIRFOIL CREATION TOOLS"""
# Author: David Moeller Sztajnbok
# Date:   July 2023

from xfoil import polar


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

    return foilPolar
