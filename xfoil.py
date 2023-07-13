# -*- coding: utf-8 -*-

"""RUN XFOIL IN PYTHON"""
# Author:   J. Hahn, September 2019
# Modified: David Moeller Sztajnbok, July 2023

import os
import subprocess

import numpy as np
import subprocess as sp
import re


def polar(afile, re, *args,**kwargs):
    """calculate airfoil polar and load results
    
    Parameters
    ----------
    afile: string
        path to aifoil dat file
    re: float
        fixed reynoldsnumber for polar calculation
    *args, **kwargs
        have a look at calcpolar for further information
        
    Returns
    -------
    dict
        airfoil polar
    """
    calc_polar(afile, re,'polar.txt', *args, **kwargs)
    data = read_polar('polar.txt')
    delete_polar('polar.txt')
    return data


def calc_polar(afile, re, polarfile, alfaseq=[], clseq=[], refine=True, max_iter=100, n=None, loud=True, visual=True):
    """run xfoil to generate polar file
    
    Parameters
    ----------
    afile: string
        path to airfoil dat file
    re: float
        fixed reynoldsnumber
    alfaseq: iterateable, optional
        sequence of angles of attack
    clseq: iterateable, optional
        sequence of lift coefficients (either those or alfaseq must be defined)
    refine: bool
        shall xfoil refine airfoil
    maxiter: int
        maximal number of boundary layer iterations
    n: int
        boundary layer parameter
    """
    
    import subprocess as sp
    import numpy as np
    import sys,os
    
    if(os.name == 'posix'):
        xfoilbin = 'xfoil'
    elif(os.name == 'nt'):
        xfoilbin = 'xfoil.exe'
    else:
        print(f'The operating system {os.name} is not supported')
    
    
    pxfoil = sp.Popen([xfoilbin], stdin=sp.PIPE, stdout=None if loud else sp.DEVNULL, stderr=None)
    
    def write2xfoil(string):
        if(sys.version_info > (3,0)):
            string = string.encode('ascii')
            
        pxfoil.stdin.write(string)

    if not visual:
        write2xfoil('PLOP\nG F\n\n')

    if(afile.isdigit()):
        write2xfoil('NACA ' + afile + '\n')
    else:
        write2xfoil('LOAD ' + afile + '\n')
        
        if(refine):
            write2xfoil('GDES\n')
            write2xfoil('CADD\n')
            write2xfoil('\n')
            write2xfoil('\n')
            write2xfoil('\n')
            write2xfoil('X\n ')
            write2xfoil('\n')
            write2xfoil('PANEL\n')

    write2xfoil('OPER\n')
    if n != None:
        write2xfoil('VPAR\n')
        write2xfoil('N '+str(n)+'\n')
        write2xfoil('\n')
    write2xfoil('ITER '+str(max_iter)+'\n')
    write2xfoil('VISC\n')
    write2xfoil(str(re) + '\n')
    write2xfoil('PACC\n')
    write2xfoil('\n')
    write2xfoil('\n')
    for alfa in alfaseq:
        write2xfoil('A ' + str(alfa) + '\n')
    for cl in clseq:
        write2xfoil('CL ' + str(cl) + '\n')
    write2xfoil('PWRT 1\n')
    write2xfoil(polarfile + '\n')
    write2xfoil('\n')

    try:
        pxfoil.communicate(str('quit').encode('ascii'), timeout=60)
    except subprocess.TimeoutExpired:
        pxfoil.kill()


def read_polar(infile):
    """read xfoil polar results from file
    
    Parameters
    ----------
    infile: string
        path to polar file
     
    Returns
    -------
    dict
        airfoil polar splitted up into dictionary
    """
    
    regex = re.compile('(?:\s*([+-]?\d*.\d*))')
    
    with open(infile) as f:
        lines = f.readlines()
        
        a           = []
        cl          = []
        cd          = []
        cdp         = []
        cm          = []
        xtr_top     = []
        xtr_bottom  = []
        
        
        for line in lines[12:]:
            linedata = regex.findall(line)
            a.append(float(linedata[0]))
            cl.append(float(linedata[1]))       
            cd.append(float(linedata[2]))
            cdp.append(float(linedata[3]))
            cm.append(float(linedata[4]))
            xtr_top.append(float(linedata[5]))
            xtr_bottom.append(float(linedata[6]))
            
        data = {'a': np.array(a), 'cl': np.array(cl) , 'cd': np.array(cd), 'cdp': np.array(cdp),
             'cm': np.array(cm), 'xtr_top': np.array(xtr_top), 'xtr_bottom': np.array(xtr_bottom)}
        
        return data


def delete_polar(infile):
    """ deletes polar file """
    os.remove(infile)
