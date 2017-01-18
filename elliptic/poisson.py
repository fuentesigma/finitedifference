#!/usr/bin/env python
# Author:  J Fuentes
# Contact: me@fvnts.ch
"""
    
    Poisson Equation  2D
    main file
    
    """
# --------------------------------------------------------------------------------/
import h5py
import engine
import graphs
# --------------------------------------------------------------------------------/
if __name__ == "__main__":
    
    # rectangular domain
    a = -20.0
    b =  20.0

    # nodes
    m = 64

    # number of iterations
    n = 100
    
    # h5 file name
    name = 'poisson.h5'
    
    # SOR algorithm
    with engine.Timer():
        u, x, y = engine.method(a, b, m, n)

    # store data
    with h5py.File(name, 'w') as hf:

        sgrp = hf.create_group('solution')
        cgrp = hf.create_group('coordinates')

        sgrp.create_dataset('u', data = u, compression="gzip")
        cgrp.create_dataset('x', data = x, compression="gzip")
        cgrp.create_dataset('y', data = y, compression="gzip")

        hf.close()

    # visualization
    graphs.wireh5(name)
# --------------------------------------------------------------------------------/
# eof
# --------------------------------------------------------------------------------/
