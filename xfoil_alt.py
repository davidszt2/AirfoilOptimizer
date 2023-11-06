"""
Custom tools for running XFOIL

@Author:    David Moeller Sztajnbok
@Date:      November, 2023
"""

import subprocess
import os

class AirfoilPolar:
    def __init__(self, alpha, CL, CD, CDp, CM, Top_Xtr, Bot_Xtr):
        self.alpha = alpha
        self.CL = CL
        self.CD = CD
        self.CDp = CDp
        self.CM = CM
        self.Top_Xtr = Top_Xtr
        self.Bot_Xtr = Bot_Xtr

def parse_polar_file(filename):
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

def run_xfoil(routine, xfoil_path='./xfoil'):
    process = subprocess.Popen(xfoil_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(routine)

    if os.path.exists('polar.dat'):
        polar_data = parse_polar_file('polar.dat')
        os.remove('polar.dat')
    else:
        print(f"Error running XFOIL: {stderr}")
        polar_data = None

    if os.path.exists('polar.dump'):
        os.remove('polar.dump')

    return polar_data

def alpha_range(airfoil, Re, alpha_start, alpha_end, alpha_increment):
    routine = f"""LOAD {airfoil}
                OPER
                Visc {Re}
                PACC
                polar.dat
                polar.dump
                ASEQ {alpha_start} {alpha_end} {alpha_increment}
                """
    return run_xfoil(routine)

def cl_range(airfoil, Re, cl_start, cl_end, cl_increment):
    routine = f"""LOAD {airfoil}
                OPER
                Visc {Re}
                PACC
                polar.dat
                polar.dump
                CSEQ {cl_start} {cl_end} {cl_increment}
                """
    return run_xfoil(routine)

def single_cl(airfoil, Re, CL):
    routine = f"""LOAD {airfoil}
                OPER
                Visc {Re}
                PACC
                polar.dat
                polar.dump
                CL {CL}
                """
    return run_xfoil(routine)

def single_alpha(airfoil, Re, alpha):
    routine = f"""LOAD {airfoil}
                OPER
                Visc {Re}
                PACC
                polar.dat
                polar.dump
                A {alpha}
                """
    return run_xfoil(routine)

# alpha_range_polar = alpha_range('clarky.dat', 1e6, 0, 15, 0.5)
