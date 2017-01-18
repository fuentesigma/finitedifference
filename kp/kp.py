#!/usr/bin/env python
# Author:  J Fuentes 
# Contact: me@fvnts.ch

"""

    Kadomtsev--Petviashvili I Equation

"""

__author__    = "J Fuentes"
__copyright__ = "Copyright 2016, www.fvnts.ch"

# --------------------------------------------------------------------------------/
import os
import h5py
import time
import numpy as np

from sys import *
from pylab import *
from scipy import *

from numpy import asmatrix as MX
from scipy.sparse import spdiags
# --------------------------------------------------------------------------------/
os.system('cls' if os.name == 'nt' else 'clear')
# --------------------------------------------------------------------------------/
# time and space domain
a = -15.0
b =  15.0
T =  4.0

# nodes 
m = 128

# space width
h = (b - a) / (1.0 + m)

# time width
k = 0.001 * h

# proper widths
E = k / (2.0*h)
F = k / (2.0*h**3)

# time steps
n = int(round(T / k) * 0.1)

# interval between steps stored
snap = 50

# h5file
name = 'kp.h5'
# --------------------------------------------------------------------------------/
# spacial coordinates
x = y = np.linspace(a, b, m)
X , Y = meshgrid(x, y)

# vector solution with phantom boundaries
u = np.zeros((m + 4, m + 4))
U = np.zeros((m + 4)*(m + 4))
# structure
o = np.ones(m)
# --------------------------------------------------------------------------------/
def f(x, y, t, l, m):
    """
    lump soliton
    l, m, r are shape factors
    """   
    #p = ( -(x - x0)**2 + r**2 * (y - y0)**2 + r**(-2) )
    #q = (  (x - x0)**2 + r**2 * (y - y0)**2 + r**(-2) )**2
    
    p =  -( x + l*y + 3*(l**2 - m**2)*t )**2  + m**2 * (y - 6*l*t )**2 + m**(-2)
    q = ( ( x + l*y + 3*(l**2 - m**2)*t )**2  + m**2 * (y - 6*l*t )**2 + m**(-2) )**2
    
    return 4.0 * p / q
# --------------------------------------------------------------------------------/
def solver(u):
    """
    implicit Crank-Nicolson method
    """
    aL = (6.0*E*u[2:-2,2:-2] - 4.0*F - 1.0 ).T.reshape(-1)
    a0 = (6.0*(E + F) - 12.0*E*u[2:-2,2:-2]).T.reshape(-1)
    aR = (6.0*E*u[2:-2,2:-2] - 4.0*F + 1.0 ).T.reshape(-1)
    
    # blocks 
    A = spdiags(
        [F*o - 3*E*o, aL, a0, aR, F*o - 3*E*o],
        [-2, -1, 0, 1, 2], 
        m * m, m * m).toarray()

    
    B = (u[3:-1,2:-2] - u[1:-3,2:-2] - 
         F*(u[:-4,2:-2] - 4*u[1:-3,2:-2] + 6*u[2:-2,2:-2] - 4*u[3:-1,2:-2] + u[4:,2:-2] ) +
         3*E*( u[2:-2,2:-2+1] - 2*u[2:-2,2:-2] + u[2:-2,2:-2-1] )
        ).T.reshape(-1)   
    # solve linear system
    return np.asarray(MX(A).I * MX(B).T)[:,0]
# --------------------------------------------------------------------------------/
# method
# initial condition u(x,y,t0) = u(x,y)
u[2:-2, 2:-2] = f(X, Y, 0, 1, 1.25)
U = u.T.reshape(-1)
# --------------------------------------------------------------------------------/
tic = time.clock()
dat = h5py.File(name, 'w')

for i in range(n):
    
    if (i % snap == 0):
    
        dat.create_dataset('u_' + str(i), data = u[2:-2, 2:-2], compression="gzip")
    
    for j in range(2, m + 1):
        
        u = solver(u)
    
    # --------------------/
    # status 
    
    done = i/(1.0 * n) * 100.0
    stdout.write(">> STEP %d OF %d | PROGRESS %.2f %% %s " %(i, n, done, "\r"))
    stdout.flush()
    
dat.close()
# --------------------------------------------------------------------------------/
# elapsed time
toc = time.clock()
# --------------------------------------------------------------------------------/
# store data
with h5py.File(name, 'a') as hf:
    cgrp = hf.create_group('coordinates')
    
    cgrp.create_dataset('x', data = X, compression="gzip")
    cgrp.create_dataset('y', data = Y, compression="gzip")
    
    hf.close()
# --------------------------------------------------------------------------------/
print '\n '
print '\n --------------------'
print '\n ELAPSED TIME =', toc - tic
print '\n --------------------'
print '\n '
# --------------------------------------------------------------------------------/
# eof
# --------------------------------------------------------------------------------/