"""
Custom tools for running XFOIL

@Author:    David Moeller Sztajnbok
@Date:      November, 2023
"""

import subprocess
import os
import numpy as np


class AirfoilPolar:
    def __init__(self, alpha, CL, CD, CDp, CM, Top_Xtr, Bot_Xtr):
        self.alpha = alpha
        self.CL = CL
        self.CD = CD
        self.CDp = CDp
        self.CM = CM
        self.Top_Xtr = Top_Xtr
        self.Bot_Xtr = Bot_Xtr
        self.CLCD = list(np.array(CL)/np.array(CD))


def parsePolar(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()[12:]

    alpha, CL, CD, CDp, CM, Top_Xtr, Bot_Xtr = [], [], [], [], [], [], []
    for line in lines:
        parts = line.split()
        alpha.append(float(parts[0]))
        CL.append(float(parts[1]))
        CD.append(float(parts[2]))
        CDp.append(float(parts[3]))
        CM.append(float(parts[4]))
        Top_Xtr.append(float(parts[5]))
        Bot_Xtr.append(float(parts[6]))

    return AirfoilPolar(alpha, CL, CD, CDp, CM, Top_Xtr, Bot_Xtr)


def runXFOIL(routine, xfoilPath='./xfoil'):
    process = subprocess.Popen(xfoilPath, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(routine, timeout=15)

    if os.path.exists('polar.dat'):
        polar = parsePolar('polar.dat')
        os.remove('polar.dat')
    else:
        print(f"Error running XFOIL: {stderr}")
        polar = None

    if os.path.exists('polar.dump'):
        os.remove('polar.dump')

    return polar


def alphaRange(airfoil, Re, alphaStart, alphaEnd, alphaStep):
    routine = f"""LOAD {airfoil}
                OPER
                Visc {Re}
                PACC
                polar.dat
                polar.dump
                ASEQ {alphaStart} {alphaEnd} {alphaStep}
                """
    return runXFOIL(routine)


def CLRange(airfoil, Re, CLStart, CLEnd, CLStep):
    routine = f"""LOAD {airfoil}
                OPER
                Visc {Re}
                PACC
                polar.dat
                polar.dump
                CSEQ {CLStart} {CLEnd} {CLStep}
                """
    return runXFOIL(routine)


def singleCL(airfoil, Re, CL):
    routine = f"""LOAD {airfoil}
                OPER
                Visc {Re}
                PACC
                polar.dat
                polar.dump
                CL {CL}
                """
    return runXFOIL(routine)


def singleAlpha(airfoil, Re, alpha):
    routine = f"""LOAD {airfoil}
                OPER
                Visc {Re}
                PACC
                polar.dat
                polar.dump
                A {alpha}
                """
    return runXFOIL(routine)
