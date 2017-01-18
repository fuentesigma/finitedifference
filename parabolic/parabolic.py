#!/usr/bin/env python
# Author:  J Fuentes
# Contact: me@fvnts.ch

"""
    
    Parabolic solver
    main file
    
    """
import heat
# --------------------------------------------------------------------------------/

if __name__=="__main__":
    """
        dictionary
        
        boomerang      wow
        spook          strips
        """
    # mesh width
    hx = hy = 5e-3
    
    # type of initial conditions
    mode = ["wow"]
    
    # steps
    steps = 1000
    
    # shot interval
    snap = 50
    
    # evaluation
    with heat.Timer():
        heat.output(hx, hy, mode, snap, steps)
# --------------------------------------------------------------------------------/
# eof
# --------------------------------------------------------------------------------/