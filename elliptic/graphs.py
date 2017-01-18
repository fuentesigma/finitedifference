#!/usr/bin/env python
# Author:  J Fuentes
# Contact: me@fvnts.ch
"""
    
    Poisson Equation  2D
    plots
    
    """
# --------------------------------------------------------------------------------/
import h5py
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import axes3d
# --------------------------------------------------------------------------------/
def wire(x, y, z):
    """
        function to plot from memory
        """
    fig = plt.figure(figsize=(8,5))
    axe = fig.add_subplot(111, projection='3d')
    axe.plot_wireframe(x, y, z, alpha=0.75, color='darkturquoise', rstride=2, cstride=2)
    axe.set_xlim(x.min() - 0.125, x.max() + 0.125)
    axe.set_ylim(y.min() - 0.125, y.max() + 0.125)
    axe.set_zlim(z.min() - 0.010, z.max() + 0.010)
    
    plt.show()
# --------------------------------------------------------------------------------/
def wireh5(name):
    """
        function to plot from file
        """
    with h5py.File(name,'r') as hf:
        u = np.array( hf.get('solution/u') )
        x = np.array( hf.get('coordinates/x') )
        y = np.array( hf.get('coordinates/y') )
        hf.close()

    fig = plt.figure(figsize=(8,5))
    axe = fig.add_subplot(111, projection='3d')
    axe.plot_wireframe(x, y, u, alpha=0.75, color='darkturquoise', rstride=2, cstride=2)
    axe.set_xlim(x.min() - 0.125, x.max() + 0.125)
    axe.set_ylim(y.min() - 0.125, y.max() + 0.125)
    axe.set_zlim(u.min() - 0.010, u.max() + 0.010)

    plt.show()
# --------------------------------------------------------------------------------/
# eof
# --------------------------------------------------------------------------------/
